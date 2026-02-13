# model_training.py
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Simulated training data (normal users)
normal_data = np.random.normal(loc=[3, 200, 0.5], scale=[1, 50, 0.1], size=(100, 3))

# Add some anomalies (bots)
anomalies = np.array([
    [0, 0, 0],   # no movement, no scroll, no typing
    [10, 1000, 0],  # super fast unnatural behavior
])

X = np.vstack([normal_data, anomalies])

# Train Isolation Forest
clf = IsolationForest(contamination=0.05, random_state=42)
clf.fit(X)

# Save model
joblib.dump(clf, "anomaly_model.pkl")
print("✅ Model trained and saved.")
