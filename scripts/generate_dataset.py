import pandas as pd
import numpy as np
import os

# Ensure the directory exists
os.makedirs('data/training', exist_ok=True)

def generate_better_data(n=200): # Increase to 200 for better accuracy
    data = []
    for _ in range(n):
        is_malicious = np.random.choice([0, 1], p=[0.7, 0.3])
        
        if is_malicious:
            # Attacks: High everything
            entropy = np.random.uniform(7.5, 8.0) 
            delta = np.random.uniform(3.0, 5.0)    # Massive sudden jump
            renamed = np.random.choice([0, 1], p=[0.2, 0.8]) # Usually renames
            freq = np.random.randint(20, 100)      # High speed
        else:
            # Safe: Mix of low and medium
            # Some safe files (like zip) have high entropy but LOW frequency/delta
            entropy = np.random.uniform(2.0, 7.0) 
            delta = np.random.uniform(0.0, 1.5)    
            renamed = 0
            freq = np.random.randint(1, 10)
            
        data.append([entropy, delta, renamed, freq, is_malicious])

    df = pd.DataFrame(data, columns=['entropy', 'delta', 'renamed', 'frequency', 'label'])
    df.to_csv('data/training/ransomware_behavior.csv', index=False)
    print("📊 Dataset generated: data/training/ransomware_behavior.csv")

if __name__ == "__main__":
    generate_better_data(200)