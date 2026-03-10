import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_reply(message, sender=None):
    """
    Uses OpenAI ChatCompletion when OPENAI_API_KEY is set.
    Otherwise falls back to simple rule-based responses.
    """
    if not message:
        return "Sorry, I didn't catch that. Can you repeat?"

    if OPENAI_API_KEY:
        try:
            import openai
            openai.api_key = OPENAI_API_KEY
            prompt = [
                {"role": "system", "content": "You are an AI receptionist. Be concise, polite, and helpful."},
                {"role": "user", "content": f"Caller: {message}"}
            ]
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt,
                max_tokens=150,
                temperature=0.2
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            # on errors, fall back
            pass

    text = message.lower()
    if "hours" in text or "open" in text:
        return "Our office hours are Mon–Fri, 9am–5pm. Can I help you with anything else?"
    if "appointment" in text or "book" in text or "schedule" in text:
        return "I can help book appointments. What date or time are you looking for?"
    if "price" in text or "cost" in text:
        return "Please tell me which service you're asking about and I'll provide details."
    return "Thanks — I received your message. A human will follow up soon."