import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class RewindBrain:
    def __init__(self, data_path='data/training/ransomware_behavior.csv'):
        # Using 50 trees for a balance of accuracy and speed on AMD hardware
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.data_path = data_path
        self.is_trained = False

    def train(self):
        """Loads the CSV dataset and trains the behavioral model."""
        if not os.path.exists(self.data_path):
            print(f"!!!!Error: Training data not found at {self.data_path}")
            return False
        
        try:
            df = pd.read_csv(self.data_path)
            # Features: Entropy, Entropy Delta, Renamed Flag, Write Frequency
            X = df[['entropy', 'delta', 'renamed', 'frequency']]
            y = df['label']
            
            self.model.fit(X, y)
            self.is_trained = True
            print(f"AI Brain: Successfully trained on {len(df)} behavioral samples.")
            return True
        except Exception as e:
            print(f"!!!!Training failed: {e}")
            return False

    def predict_threat(self, entropy, delta, renamed, frequency):
        """
        Takes real-time features and returns a probability score (0.0 to 1.0).
        """
        if not self.is_trained:
            # Fallback to a basic check if model isn't ready
            return 1.0 if entropy > 7.5 else 0.0
        
        features = pd.DataFrame([[entropy, delta, int(renamed), frequency]],
                                columns=['entropy', 'delta', 'renamed', 'frequency']) 
        # Returns the probability of the 'Malicious' class (index 1)
        probability = self.model.predict_proba(features)[0][1]
        return probability