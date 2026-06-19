import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pickle
import os

class FraudDetectionModel:
    def __init__(self):
        self.model_path = 'fraud_model.pkl'
        self.data_path = 'my_emails.csv' # NAYI LINE: Hamari data file ka naam
        self.pipeline = None
        
        # Agar model pehle se train nahi hai, toh automatically train karega
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.train_initial_model()

    def train_initial_model(self):
        print("Training Machine Learning Fraud Detection Model from CSV Data...")
        
        # NAYA LOGIC: CSV file se data padhna
        if not os.path.exists(self.data_path):
            print(f"Error: {self.data_path} file nahi mili! Pehle apna email data isme save karo.")
            return

        try:
            # Pandas ka use karke CSV file read kar rahe hain
            df = pd.DataFrame(pd.read_csv(self.data_path))
            print(f"Successfully loaded {len(df)} emails for training.")
        except Exception as e:
             print(f"Error reading CSV file: {e}")
             return
        
        # Pipeline: Text ko numbers me convert karna (TF-IDF) -> Random Forest Model
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        # Model ko train karna (CSV ke 'text' aur 'label' columns use karke)
        self.pipeline.fit(df['text'], df['label'])
        
        # Model ko save karna taaki baar-baar train na karna pade
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.pipeline, f)
            
        print("✅ ML Model Trained from your Custom Data and Saved Successfully!")

    def load_model(self):
        with open(self.model_path, 'rb') as f:
            self.pipeline = pickle.load(f)

    def analyze_email(self, email_text):
        """
        Email ko analyze karke uski category batata hai
        """
        if not self.pipeline:
             return {"is_fraud": False, "category": "Model Not Trained", "confidence_score": 0}

        prediction = self.pipeline.predict([email_text])[0]
        
        # Probability (Confidence Score) nikalna
        probabilities = self.pipeline.predict_proba([email_text])[0]
        max_prob = max(probabilities) * 100
        
        is_fraud = "Fraud" in prediction
        
        return {
            "is_fraud": is_fraud,
            "category": prediction,
            "confidence_score": round(max_prob, 2)
        }

# Testing ke liye
if __name__ == "__main__":
    detector = FraudDetectionModel()
    
    test_email = "Your electricity bill is due. Click here to pay immediately to avoid disconnection."
    result = detector.analyze_email(test_email)
    
    print("\n--- ML Email Analysis ---")
    print(f"Email: {test_email}")
    print(f"Result: {result}")