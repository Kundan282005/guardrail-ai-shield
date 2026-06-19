import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from groq import Groq
from ml_fraud_detector import FraudDetectionModel # Hamara ML model yaha import ho raha hai

# 1. Environment variables load karein
load_dotenv()

app = Flask(__name__)

# Groq API Key config
groq_key = os.environ.get('GROQ_API_KEY')
if not groq_key:
    raise ValueError("ERROR: .env file mein GROQ_API_KEY nahi mili!")

client = Groq(api_key=groq_key)

# 2. Fraud Detection Model load karein
print("Initializing Fraud Detection Model...")
fraud_detector = FraudDetectionModel()
print("Fraud Detection System Ready.")

# 🌐 Yeh route hamari website ka Frontend (HTML) dikhayega
@app.route('/')
def home():
    return render_template('index.html')

# ⚙️ Yeh API route Frontend se email lega, ML se fraud check karega, aur AI se answer lakar dega
@app.route('/api/summarize', methods=['POST'])
def summarize_email():
    data = request.get_json()
    email_text = data.get('email_text', '')

    if not email_text:
        return jsonify({"error": "Please provide email text"}), 400

    try:
        # STEP 1: Pehle Machine Learning se check karo ki fraud hai ya nahi
        fraud_analysis = fraud_detector.analyze_email(email_text)
        is_fraud = fraud_analysis['is_fraud']
        fraud_category = fraud_analysis['category']
        confidence = fraud_analysis['confidence_score']
        
        # STEP 2: Llama-3.1 ko prompt dena
        # Agar fraud detect hua hai, to prompt me explicit warning add kardo
        fraud_context = ""
        if is_fraud:
            fraud_context = f"\nWARNING: A Machine Learning model has flagged this email as a potential {fraud_category} (Confidence: {confidence}%). " \
                            f"Please prominently warn the user about this in the summary and suggest them not to click any links or share sensitive information."
        
        prompt = f"""
        You are an expert executive assistant and cybersecurity analyst. 
        Analyze the following email and provide:
        1. A concise summary in exactly 3 bullet points. {fraud_context}
        2. A polite, professional, and actionable reply draft. (If it's a scam, draft a polite refusal or suggest deleting the email).
        
        Format the output strictly as:
        SUMMARY:
        - [Point 1]
        - [Point 2]
        - [Point 3]
        
        REPLY:
        [Your reply draft here]
        
        Email Content:
        {email_text}
        """
        
        # Llama 3.1 API Call
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional AI assistant and cybersecurity expert."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.3
        )
        text_output = chat_completion.choices[0].message.content
        
        # Output ko alag-alag karna
        parts = text_output.split("REPLY:")
        summary = parts[0].replace("SUMMARY:", "").strip()
        reply = parts[1].strip() if len(parts) > 1 else "Reply draft generate nahi ho paya."
        
        return jsonify({
            "summary": summary,
            "reply": reply,
            "fraud_analysis": fraud_analysis # Frontend ko data bhejna
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Flask server ko start karna
    app.run(debug=True)