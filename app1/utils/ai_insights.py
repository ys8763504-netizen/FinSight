import requests
from django.conf import settings

def generate_insights(expenses, total, categories, budgets, goals):
    try:

        prompt = f"""
You are a smart financial assistant.

Total Spending: ₹{total}
Categories: {categories}
Budgets: {budgets}
Goals: {goals}
Expenses: {expenses}

Give financial insights with tips and emojis.
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

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {result}"

    except Exception as e:
        return f"Error: {str(e)}"