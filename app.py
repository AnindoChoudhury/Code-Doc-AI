import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    try:
        code = request.json['code']
        
        prompt = f"""
        You are an expert C++ programmer and technical writer.
        Your task is to generate clear and concise documentation for the following C++ function.

        The documentation must be in Doxygen format. It should include:
        1. A brief, one-sentence summary of the function's purpose.
        2. A detailed explanation of what the function does.
        3. A list of all parameters (@param), their types, and what they represent.
        4. A description of the return value (@return).

        Here is the C++ function:
        ```cpp
        {code}
        ```
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(prompt)
        
        ai_response = response.text
        
        return jsonify({'status': 'success', 'documentation': ai_response})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to generate documentation.'}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)