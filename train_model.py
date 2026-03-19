import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# LOAD DATASET
data = pd.read_csv("student_performance.csv")

print("Original shape:", data.shape)

# 🔥 TAKE SMALL SAMPLE (FAST TRAINING)
data = data.sample(n=5000, random_state=42)  # reduce size

print("Sampled shape:", data.shape)

# FEATURES (CORRECT COLUMNS)
X = data[['weekly_self_study_hours', 'attendance_percentage', 'class_participation']]
y = data['grade']

# ENCODE TARGET
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔥 LIGHT MODEL (FAST)
model = RandomForestClassifier(
    n_estimators=20,   # reduced trees
    max_depth=10,      # limit depth
    random_state=42
)

# TRAIN
model.fit(X_train, y_train)

# SAVE
joblib.dump(model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")

print("✅ Model trained and saved successfully!")