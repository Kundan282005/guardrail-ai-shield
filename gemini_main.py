import os
import logging
from typing import Dict, Optional
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import generation_types

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

def process_email(email_text: str) -> Dict[str, Optional[str]]:
    """
    Processes an email to generate a summary and draft a reply using Google Gemini.

    Args:
        email_text (str): The content of the email to process.

    Returns:
        Dict[str, Optional[str]]: A dictionary containing the "summary" and "reply".
            Keys will have None if processing fails.
    """
    result = {"summary": None, "reply": None}
    
    # Load API key from environment
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        logging.error("GEMINI_API_KEY not found in environment variables.")
        return result

    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-pro')

    except Exception as e:
        logging.error(f"Failed to initialize Gemini client: {e}")
        return result

    try:
        # Generate summary
        summary_prompt = (
            "Summarize the following email in exactly 3 concise bullet points:\n\n"
            f"{email_text}"
        )
        
        summary_response = model.generate_content(summary_prompt)
        result["summary"] = summary_response.text.strip()

        # Draft reply
        reply_prompt = (
            "Draft a polite, professional, and actionable reply to the following email:\n\n"
            f"{email_text}"
        )

        reply_response = model.generate_content(reply_prompt)
        result["reply"] = reply_response.text.strip()

    except generation_types.StopCandidateException as e:
        logging.error(f"Generate content was stopped: {e}")
    except Exception as e:
        logging.error(f"An API or unexpected error occurred: {e}")

    return result

if __name__ == "__main__":
    sample_email = """Subject: Project Alpha Delay & Resource Reallocation

Hi Team,

I hope this email finds you well. I am writing to inform you that we will be experiencing an unavoidable delay in the delivery of Project Alpha. Due to unexpected technical hurdles during the integration phase with the legacy CRM system, our timeline has been pushed back by approximately two weeks. The new expected delivery date is now November 15th. 

To mitigate further delays, I have decided to reallocate two developers from Project Beta to assist with the integration tasks on Project Alpha. This should not significantly impact Project Beta, but please keep a close eye on your respective sprints and let me know if you foresee any critical bottlenecks. 

Could we please schedule a brief 15-minute sync this Thursday afternoon to discuss this pivot in more detail? I would like to make sure we are all fully aligned on the next steps and ensure that our clients are given a clear, unified message. Let me know what times work best for you.

Best regards,
Sarah Jenkins
Director of Engineering"""

    logging.info("Processing email with Gemini...")
    output = process_email(sample_email)

    print("\n" + "="*50)
    print("OUTPUT SUMMARY:")
    print("="*50)
    print(output.get("summary"))

    print("\n" + "="*50)
    print("OUTPUT REPLY:")
    print("="*50)
    print(output.get("reply"))
