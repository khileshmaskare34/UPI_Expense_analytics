import joblib
import os
from .preprocess import clean_text

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/category_model.pkl")
VEC_PATH = os.path.join(os.path.dirname(__file__), "models/vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

def predict_category(description: str) -> int:
    """Predict category_id from text description."""
    cleaned = clean_text(description)
    vec = vectorizer.transform([cleaned])
    return int(model.predict(vec)[0])
