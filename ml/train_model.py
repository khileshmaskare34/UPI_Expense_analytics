import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

from preprocess import clean_text

DATASET_PATH = "data/dataset.csv"
MODEL_PATH = "models/category_model.pkl"
VEC_PATH = "models/vectorizer.pkl"

print("Data set path_:", DATASET_PATH)
# Load dataset
df = pd.read_csv(DATASET_PATH)

# Clean text
df["clean_desc"] = df["description"].apply(clean_text)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_desc"], df["category"], test_size=0.2, random_state=42
)


# TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Train classifier
model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

# Save model and vectorizer
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VEC_PATH)

print("Model training complete.")
