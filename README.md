# 🛡️ GUARDRAIL PRO - Enterprise AI Email Fraud Shield

An advanced, Full-Stack Machine Learning & AI-powered application designed to detect, intercept, and neutralize email fraud vectors (like Phishing, BEC, Ransomware) using custom ML models and Llama-3.1 LLM.

## 🚀 Features
* **Custom Machine Learning Model:** Trained on local `.csv` datasets to identify 80+ types of email scams.
* **Llama-3.1 Integration:** Generates 3-point forensic summaries of incoming payloads.
* **Automated Mitigation:** Locks the reply drafting feature if a high-confidence threat vector is detected.
* **Cyberpunk Dashboard:** Premium React/Vite-based dark mode UI for security monitoring.

## 🛠️ Tech Stack
* **Frontend:** React, Vite, Tailwind CSS (v4)
* **Backend:** Python, Flask
* **AI/ML:** Scikit-Learn (Random Forest, TF-IDF), Pandas, Groq API (Llama-3.1)

## 💡 How It Works
1. User pastes raw email text into the input payload analyzer.
2. The `FraudDetectionModel` scans the text using NLP to calculate a confidence score.
3. If safe, a polite automated reply is drafted. If fraud, an explicit protocol lock is engaged to prevent user error.