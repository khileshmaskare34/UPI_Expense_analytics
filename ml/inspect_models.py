import joblib

model = joblib.load("models/category_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

print("Model loaded successfully.")
print("Model type:", type(model))
print("Vectorizer loaded successfully.")
print("Vectorizer type:", type(vectorizer))
