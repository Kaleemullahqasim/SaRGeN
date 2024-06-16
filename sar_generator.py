# sar_generator.py
import json
from openai import OpenAI

# Set up the LLM client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def generate_sar_narrative(customer_id, violations, transactions):
    try:
        prompt = f"""
        You are a compliance officer tasked with generating a Suspicious Activity Report (SAR) narrative.

        Customer ID: {customer_id}

        The customer has violated the following red flag rules: {', '.join(violations)}.

        Below are the transaction details:

        {json.dumps(transactions, indent=2)}

        Please generate a comprehensive SAR narrative that includes:
        1. A clear description of each suspicious activity and why it is considered suspicious (Who conducted the activity? What types of transactions were involved?).
        2. Specific transaction details that highlight the suspicious behavior (When did the transactions occur? Where did the activity take place?).
        3. Any patterns or connections between the transactions.
        4. The potential implications of these activities and why they raise red flags (Why does the Bank think the activity is suspicious? How did the suspicious activity occur?).
        5. An introductory paragraph providing information on the financial institution, the subject(s) of the SAR, the account(s) involved, the date range of the suspicious activity, the nature of the suspicious activity, and the total amount of the suspicious activity.
        6. A conclusion paragraph indicating any follow-up planned by the institution and any other pertinent information.

        Ensure the narrative is clear, concise, and suitable for submission to regulatory authorities.
        EXTREMELY IMPORTANT: Ensure that the narrative is compliant with the Bank Secrecy Act (BSA) and other relevant regulations, and it should must follow the offical format.
        """
        completion = client.chat.completions.create(
            model="microsoft/Phi-3-mini-4k-instruct-gguf",
            messages=[
                {"role": "system", "content": "You are a compliance officer EXPERT in writing and generating SAR narratives."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating SAR narrative: {e}"
