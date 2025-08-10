import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the Google AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    try:
        # Get the C++ code from the incoming request
        code = request.json['code']
        
        # The prompt is the same as before!
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

        # Initialize the Generative Model (e.g., Gemini Flash)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content using the Gemini model
        response = model.generate_content(prompt)
        
        # Extract the AI's response text
        ai_response = response.text
        
        # Send the AI's response back to the client
        return jsonify({'status': 'success', 'documentation': ai_response})

    except Exception as e:
        # Handle potential errors
        print(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to generate documentation.'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)