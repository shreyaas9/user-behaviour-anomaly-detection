import joblib
import numpy as np

clf = joblib.load("anomaly_model.pkl")

# Test human-like
human = np.array([[3, 300, 0.4]])
print("Human:", clf.predict(human))  # Expected: [1]

# Test bot-like (idle)
bot_idle = np.array([[0, 0, 0]])
print("Bot Idle:", clf.predict(bot_idle))  # Expected: [-1]

# Test bot-like (super fast)
bot_fast = np.array([[12, 1500, 0]])
print("Bot Fast:", clf.predict(bot_fast))  # Expected: [-1]
