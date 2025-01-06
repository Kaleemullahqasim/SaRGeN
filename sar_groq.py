import json
from groq import Groq

def generate_sar_narrative(customer_id, rules, transactions):
    prompt = f"""
Generate a professional Suspicious Activity Report (SAR) narrative using the following format and guidelines:

SUMMARY OF SUSPICIOUS ACTIVITY
[Provide a concise overview including:
- Nature and pattern of suspicious activities
- Total value of suspicious transactions
- Time period of suspicious activity]

CUSTOMER DETAILS
[Include:
- Account type and relationship
- Account history and business type
- Relevant customer background]

TRANSACTION PATTERNS
[Detail:
- Analysis of transaction frequency
- Transaction amounts and patterns
- Unusual behaviors or deviations
- Specific examples with dates and amounts]

RED FLAGS IDENTIFIED
[For each identified rule violation ({', '.join(rules)}):
- Describe the specific violation pattern
- Provide supporting transaction evidence
- Explain why the pattern is suspicious]

CONCLUSION
[Include:
- Overall risk assessment
- Summary of primary concerns
- Recommended actions]

Guidelines:
1. Use precise, factual language
2. Avoid speculation or personal opinions
3. Focus on objective patterns and evidence
4. Format monetary values as "$X,XXX.XX"
5. Use proper date formatting (MM/DD/YYYY)
6. Maintain professional tone throughout
7. Reference specific transactions where relevant
8. Organize information in clear, logical sections

Do not include any introductory text before the first section header.
"""
    try:
        api_key = ""

        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional BSA/AML analyst writing clear, structured SAR narratives."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            stream=True,
            stop=None,
        )

        narrative = ""
        for chunk in completion:
            narrative += chunk.choices[0].delta.content or ""

        # Clean up any duplicate sections
        sections = ["SUMMARY OF SUSPICIOUS ACTIVITY", "CUSTOMER DETAILS", 
                   "TRANSACTION PATTERNS", "RED FLAGS IDENTIFIED", "CONCLUSION"]
        cleaned_narrative = ""
        seen_sections = set()
        
        current_section = None
        for line in narrative.split('\n'):
            if any(section in line for section in sections):
                section_name = next(s for s in sections if s in line)
                if section_name not in seen_sections:
                    seen_sections.add(section_name)
                    current_section = section_name
                    cleaned_narrative += f"\n\n{section_name}\n{'='*len(section_name)}\n"
                continue
            if current_section and line.strip():
                cleaned_narrative += line + "\n"

        return cleaned_narrative.strip()
    except Exception as e:
        return f"Error generating SAR narrative: {e}"
