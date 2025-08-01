from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend access

openai.api_key = "sk-your-api-key-here"  # Replace with your key

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json['query']

    prompt = f"""
You are a legal expert trained in Indian law.

User's Problem: {user_query}

Reply in this format:
Legal Status: (Legal / Illegal / Partially Legal)
Law: (Related law/section)
Solution: (Simple action the user should take)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful Indian legal assistant bot."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response['choices'][0]['message']['content']
    return jsonify({"answer": answer})