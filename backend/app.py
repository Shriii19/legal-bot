from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow frontend access

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json['query']
    
    # For demo purposes, return a mock response
    # Replace this section with actual OpenAI integration when you have a valid API key
    answer = f"""
Legal Status: Please consult a lawyer for accurate advice
Law: This is a demo response. Replace with actual OpenAI integration.
Solution: To get real legal advice, please:
1. Add your OpenAI API key to the environment
2. Uncomment the OpenAI integration code below

Your query was: {user_query}
"""
    
    return jsonify({"answer": answer})

# Uncomment the following lines when you have a valid OpenAI API key:
"""
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here")
)

@app.route('/ask', methods=['POST'])
def ask_with_openai():
    user_query = request.json['query']

    prompt = f\"\"\"
You are a legal expert trained in Indian law.

User's Problem: {user_query}

Reply in this format:
Legal Status: (Legal / Illegal / Partially Legal)
Law: (Related law/section)
Solution: (Simple action the user should take)
    \"\"\"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use gpt-3.5-turbo instead of gpt-4 to save costs
        messages=[
            {"role": "system", "content": "You are a helpful Indian legal assistant bot."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    return jsonify({"answer": answer})
"""

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)