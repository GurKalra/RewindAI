import os
import time
import pandas as pd  # FIXED: Added pandas import
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from brain import RewindBrain  
from shield import Shield 

# --- Setup Modules ---
brain = RewindBrain()
brain.train() 
shield = Shield(vault_path="data/vault", shadow_path="data/shadow_root")
shield.create_baseline()

file_history = {} 

# --- StreamLit setup ---
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/status.txt"):
    with open("data/status.txt", "w") as f:
        f.write("SAFE|None|0.00|0.0")

def update_training_data(features, label, threat_score):
    """Appends new real-time data to the CSV for continuous learning."""
    try:
        delta = features[1] # FIXED: Extract delta from features list
        # FIXED: Only save significant events to avoid data flooding
        if (label == 1 and threat_score > 0.5) or (label == 0 and delta > 0.1):
            new_row = pd.DataFrame([features + [label]], 
                                   columns=['entropy', 'delta', 'renamed', 'frequency', 'label'])
            new_row.to_csv('data/training/ransomware_behavior.csv', mode='a', index=False, header=False)
            print(f"🧠 AI Updated: New {('Malicious' if label==1 else 'Safe')} sample added.")
    except Exception as e:
        print(f"Could not update dataset: {e}")

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

# FIXED: Combined into one master class
class AIHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory: return
        
        time.sleep(0.1)
        filename = os.path.basename(event.src_path)
        current_entropy = calculate_entropy(event.src_path)
        current_time = time.time()

        if filename not in file_history:
            file_history[filename] = {'last_entropy': current_entropy, 'last_time': current_time, 'count': 0}
        
        hist = file_history[filename]
        delta = abs(current_entropy - hist['last_entropy'])
        freq = hist['count'] + 1 
        renamed = 0 

        # AI Prediction
        threat_score = brain.predict_threat(current_entropy, delta, renamed, freq)
        feature_list = [current_entropy, delta, renamed, freq]
        
        print(f"File: {filename} | Entropy: {current_entropy:.2f} | Threat Score: {threat_score:.2f}")

        # 4. ACTION BLOCK
        if threat_score > 0.7:
            print(f"🚨 AI ALERT: Ransomware Confidence {threat_score*100:.0f}%!")
            
            # 1. Log attack for Streamlit
            with open("data/status.txt", "w") as f:
                f.write(f"ATTACK|{filename}|{threat_score:.2f}|{current_time}")
            
            # 2. Hold state for UI to draw the spike!
            time.sleep(0.6)
            
            # 3. Restore the file
            shield.restore_file(filename)
            
            # 4. Continuous Learning (Pass the threat_score now!)
            update_training_data(feature_list, 1, threat_score)
            
            # 5. Reset baseline
            healthy_entropy = calculate_entropy(event.src_path) 
            file_history[filename] = {'last_entropy': healthy_entropy, 'last_time': current_time, 'count': 0}
            print(f"🔄 Baseline Reset: {filename} is healthy again (Entropy: {healthy_entropy:.2f})")
            
        else:
            # 1. Log safe state for Streamlit
            with open("data/status.txt", "w") as f:
                f.write(f"SAFE|{filename}|{threat_score:.2f}|{current_time}")
                
            # 2. Continuous Learning
            if delta > 0.1:
                update_training_data(feature_list, 0, threat_score)
                
            # 3. Update history normally
            file_history[filename] = {'last_entropy': current_entropy, 'last_time': current_time, 'count': freq}

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(AIHandler(), "data/vault", recursive=False)
    print("🧠 RewindAI Monitor (AI-Powered) Active...")
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: observer.stop()
    observer.join()