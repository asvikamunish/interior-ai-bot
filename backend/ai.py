from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_reply(message: str, context: dict):
    try:
        system_prompt = "You are an expert interior designer."

        response = client.chat.completions.create(
            model="llama3-8b-8192",  # ✅ FIXED MODEL
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI error occurred: {str(e)}"
