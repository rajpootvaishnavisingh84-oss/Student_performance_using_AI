import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# LOAD DATA
data = pd.read_csv("student_performance.csv")

print("Original shape:", data.shape)

# 🔥 TAKE SMALL SAMPLE (VERY IMPORTANT)
data = data.sample(n=3000, random_state=42)

print("Sampled shape:", data.shape)

# FEATURES (NO DATA LEAKAGE)
X = data[['weekly_self_study_hours', 'attendance_percentage', 'class_participation']]
y = data['grade']

# ENCODE
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 🔥 FAST MODEL
model = RandomForestClassifier(
    n_estimators=20,   # LOW TREES = FAST
    max_depth=5,       # LIMIT DEPTH
    n_jobs=-1,         # USE ALL CPU
    random_state=42
)

print("Training started...")

# TRAIN
model.fit(X_train, y_train)

print("Training completed!")

# TEST
pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("\nAccuracy:", acc)
print("\nReport:\n", classification_report(y_test, pred))

# CROSS VALIDATION (FAST)
scores = cross_val_score(model, X, y, cv=3)
print("\nCross-validation:", scores.mean())

# SAVE
joblib.dump(model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")

print("\n✅ Model saved successfully!")