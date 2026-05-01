import pandas as pd
import joblib
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

def clean_text(text):
    """Basic text cleaning."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+|[^A-Za-z\s]", "", text)
    return text.lower().strip()

def train_sentiment_model(data_path="outputs/synthetic_social_data.csv", model_dir="backend/ml_model"):
    """
    Trains a Logistic Regression model on TF-IDF features.
    """
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path, encoding='utf-8')
    
    print("Cleaning text...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Drop empty rows
    df = df[df['cleaned_text'] != ""]
    
    X = df['cleaned_text']
    y = df['sentiment']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Vectorizing text (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)
    
    print("\n--- Evaluation ---")
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))
    
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "sentiment_model.pkl")
    vec_path = os.path.join(model_dir, "vectorizer.pkl")
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)
    print(f"Success: Model and Vectorizer saved to {model_dir}/")

if __name__ == "__main__":
    train_sentiment_model()
