import os
from groq import Groq

# Read API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)


def get_ai_reply(message: str, context: dict):
    try:
        system_prompt = "You are an expert interior designer AI."

        if "room" in context:
            system_prompt += f" The room is a {context['room']}."
        if "style" in context:
            system_prompt += f" Style preference: {context['style']}."
        if "budget" in context:
            system_prompt += f" Budget info: {context['budget']}."

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI error occurred: {str(e)}"
