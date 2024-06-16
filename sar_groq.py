import json
from groq import Groq

def generate_sar_narrative(customer_id, violations, transactions):
    try:
        prompt = f"""
        You are a compliance officer tasked with generating a Suspicious Activity Report (SAR) narrative.

        Customer ID: {customer_id}

        The customer has violated the following rules: {', '.join(violations)}.

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

        api_key = "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"  # Replace with your actual API key

        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        narrative = ""
        for chunk in completion:
            narrative += chunk.choices[0].delta.content or ""

        return narrative
    except Exception as e:
        return f"Error generating SAR narrative: {e}"