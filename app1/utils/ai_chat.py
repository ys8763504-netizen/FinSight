import requests
from django.conf import settings

def generate_chat_reply(user_message, total_expense, categories, total_budget, goal_data):
    try:

        prompt = f"""
You are a smart finance AI assistant.
RULES:
- If the user greets (hello, hi, hey) → respond politely and briefly, DO NOT give financial advice.
- If user asks a finance question → use data and give insights.
- If user question is not related to finance → reply politely and guide them back.


User question:
{user_message}

User financial data:
- Total Spending: {total_expense}
- Categories: {categories}
- Total Budget: {total_budget}
- Goal data: {goal_data}

Give short, helpful financial advice.
"""

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"