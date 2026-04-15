from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_insights(expenses, total, categories, budgets, goals):
    try:
        prompt = f"""
        You are a smart financial assistant.

        User Data:

        Total Spending: ₹{total}

        Category Spending:
        {categories}

        Budgets:
        {budgets}

        Goals:
        {goals}

        Expense List:
        {expenses}

        Instructions:
        - Answer based on user data
        - Give smart insights
        - Compare expenses with budgets
        - Analyze goals progress
        - Give suggestions to save money
        - If user asks a question, answer accordingly
        - Keep response clean and readable
        Give insights with emojis and short bullet points also currency is rupee.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"