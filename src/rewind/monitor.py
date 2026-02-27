import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
from brain import RewindBrain  
from shield import Shield 

# --- Setup Modules ---
brain = RewindBrain()
brain.train() # Loads CSV and trains the Random Forest
shield = Shield(vault_path="data/vault", shadow_path="data/shadow_root")

file_history = {} # Format: {filename: {'last_entropy': float, 'last_time': float, 'count': int}}

# --- StreamLit setup ---
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/status.txt"):
    with open("data/status.txt", "w") as f:
        f.write("SAFE|None|0.00|0.0")

def update_training_data(features, label):
    """Appends new real-time data to the CSV for continuous learning."""
    try:
        new_row = pd.DataFrame([features + [label]], 
                               columns=['entropy', 'delta', 'renamed', 'frequency', 'label'])
        # Append to CSV without writing the header again
        if(label == 1 and threat_score > 0.5) or (label == 0 and delta > 0.5):
            new_row.to_csv('data/training/ransomware_behavior.csv', mode='a', index=False, header=False)
        print(f"📈 AI Updated: New {('Malicious' if label==1 else 'Safe')} sample added to dataset.")
    except Exception as e:
        print(f"⚠️ Could not update dataset: {e}")

class ContinuousLearningHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory: return
        
        time.sleep(0.1)
        filename = os.path.basename(event.src_path)
        current_entropy = calculate_entropy(event.src_path)
        current_time = time.time()

        if filename not in file_history:
            file_history[filename] = {'last_entropy': current_entropy, 'count': 0}
        
        hist = file_history[filename]
        delta = abs(current_entropy - hist['last_entropy'])
        freq = hist['count'] + 1
        renamed = 0 

        # AI Prediction
        threat_score = brain.predict_threat(current_entropy, delta, renamed, freq)
        
        # Features for the CSV
        feature_list = [current_entropy, delta, renamed, freq]

        if threat_score > 0.7:
            print(f"🚨 AI ALERT: Ransomware Confidence {threat_score*100:.0f}%!")
            shield.restore_file(filename)
            # Store as Malicious (Label 1)
            update_training_data(feature_list, 1)
            file_history[filename] = {'last_entropy': current_entropy, 'count': 0}
        else:
            print(f"✅ Safe: {filename} (Score: {threat_score:.2f})")
            # Store as Safe (Label 0) if it's a significant enough change to learn from
            if delta > 0.1:
                update_training_data(feature_list, 0)
            file_history[filename] = {'last_entropy': current_entropy, 'count': freq}

def calculate_entropy(file_path):
    try:
        if os.path.getsize(file_path) == 0: return 0
        with open(file_path, "rb") as f:
            data = f.read(1024 * 64)
            counts = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
            if len(data) == 0:
                return 0
            probs = counts / len(data)
            return -np.sum(probs[probs > 0] * np.log2(probs[probs > 0]))
    except: return 0

class AIHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory: return
        
        time.sleep(0.1)
        filename = os.path.basename(event.src_path)
        current_entropy = calculate_entropy(event.src_path)
        current_time = time.time()

        # 1. Initialize or update history for this file
        if filename not in file_history:
            file_history[filename] = {'last_entropy': current_entropy, 'last_time': current_time, 'count': 0}
        
        hist = file_history[filename]
        
        # 2. Extract AI Features
        delta = abs(current_entropy - hist['last_entropy'])
        # Simplified "Frequency": modifications per second
        freq = hist['count'] + 1 
        renamed = 0 # In this MVP version, we detect modification. Rename detection can be added via on_moved.

        # 3. Get AI Prediction
        threat_score = brain.predict_threat(current_entropy, delta, renamed, freq)
        
        print(f"File: {filename} | Entropy: {current_entropy:.2f} | Threat Score: {threat_score:.2f}")

        # 4. Action based on AI Score (e.g., > 70% confidence)
        if threat_score > 0.7:
            print(f"🚨 AI ALERT: Ransomware Confidence {threat_score*100:.0f}%! Restoring...")
            
            # 1. Restore the file
            shield.restore_file(filename)
            
            # 2. Get the NEW healthy entropy to reset the baseline correctly
            healthy_entropy = calculate_entropy(event.src_path) 
            
            # 3. Reset history using the HEALTHY entropy
            file_history[filename] = {
                'last_entropy': healthy_entropy, 
                'last_time': current_time, 
                'count': 0
            }
            print(f"🔄 Baseline Reset: {filename} is back to healthy entropy ({healthy_entropy:.2f})")

            with open("data/status.txt", "w") as f:
                f.write(f"ATTACK|{filename}|{threat_score:.2f}|{current_time}")
        else:
            # Update history normally for safe edits
            file_history[filename] = {
                'last_entropy': current_entropy, 
                'last_time': current_time, 
                'count': freq
            }
            with open("data/status.txt", "w") as f:
                f.write(f"SAFE|{filename}|{threat_score:.2f}|{current_time}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(AIHandler(), "data/vault", recursive=False)
    print("🧠 RewindAI Monitor (AI-Powered) Active...")
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: observer.stop()
    observer.join()