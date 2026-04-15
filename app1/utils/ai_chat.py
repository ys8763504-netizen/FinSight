from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_chat_reply( user_message,total_expense,categories,total_budget,goal_data):
    try:
        prompt = f"""
        You are a smart AI assistant inside a finance app.

        User question:
        {user_message}

        User financial data:
        - Total Spending: {total_expense}
        - Categories: {categories}
        - Total Budget :{total_budget}
        - Goal data : {goal_data}

        Instructions:
        - Answer based on the user's question.
        - If it's finance-related → use the data.
        - If it's general → answer normally.
        - Keep it short and helpful.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"