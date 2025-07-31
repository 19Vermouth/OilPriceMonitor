import numpy as np
from collections import deque

class AnomalyDetector:
    def __init__(self, window_size=10, threshold=3):
        """
        Simplified anomaly detector using moving z-score
        
        Parameters:
        - window_size: Number of previous values to consider
        - threshold: Z-score threshold for anomaly detection
        """
        self.window_size = window_size
        self.threshold = threshold
        self.price_window = deque(maxlen=window_size)
        
    def detect_anomaly(self, new_price):
        self.price_window.append(new_price)
        if len(self.price_window) < self.window_size:
            return False, 0.0
            
        prices = list(self.price_window)
        mean = np.mean(prices[:-1])
        std = np.std(prices[:-1])
        z_score = (prices[-1] - mean) / std if std != 0 else 0.0
        
        print(f"DEBUG: Price={prices[-1]}, Mean={mean:.2f}, STD={std:.2f}, Z={z_score:.2f}")
        return abs(z_score) > self.threshold, z_score