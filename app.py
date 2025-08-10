import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    try:
        # Get the C++ code from the incoming request
        code = request.json['code']
        
        # This is our Prompt Engineering!
        # We create a detailed instruction for the AI.
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

        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful C++ documentation assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        # Extract the AI's response text
        ai_response = response.choices[0].message.content

        # For debugging: print the AI response to our terminal
        print("AI Response Generated.")

        # Send the AI's response back to the client
        return jsonify({'status': 'success', 'documentation': ai_response})

    except Exception as e:
        # Handle potential errors (e.g., missing API key, network issues)
        print(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to generate documentation.'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)