# import joblib
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# MODEL_PATH = os.path.join(BASE_DIR, "ml/models/category_model.pkl")
# VEC_PATH = os.path.join(BASE_DIR, "ml/models/vectorizer.pkl")

# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VEC_PATH)


# def predict_category(description: str) -> int:
#     if not description:
#         return None

#     X = vectorizer.transform([description])
#     category_id = model.predict(X)[0]
#     return int(category_id)


import joblib
from pathlib import Path

# ml_service.py → services → app → backend → project-root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "category_model.pkl"
VEC_PATH = PROJECT_ROOT / "ml" / "models" / "vectorizer.pkl"

print("PROJECT_ROOT:", PROJECT_ROOT)
print("MODEL exists:", MODEL_PATH.exists())
print("VEC exists:", VEC_PATH.exists())

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

def predict_category(description: str) -> int:
    if not description:
        return None

    X = vectorizer.transform([description])
    category_id = model.predict(X)[0]
    return int(category_id)
