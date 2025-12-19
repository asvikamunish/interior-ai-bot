import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in backend/.env")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are Aira, a professional interior designer.
You speak politely, clearly, and naturally.
You ask clarifying questions when the input is vague.
Provide practical and realistic interior design suggestions.
"""

def get_ai_reply(user_message: str, context: dict = None) -> str:
    try:
        context_text = ""

        if context and len(context) > 0:
            details = []
            for key, value in context.items():
                details.append(f"{key}: {value}")
            context_text = (
                "Known user preferences so far: "
                + ", ".join(details)
                + ". Use this information naturally in your response."
            )

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": context_text},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI error occurred: {str(e)}"
