from flask import Flask, request, jsonify
import json
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def generate_response(user_input, data):
    for pattern_response in data:
        pattern = pattern_response['pattern']
        responses = pattern_response['responses']
        for pattern in pattern:
            if pattern.lower() in user_input.lower():
                return random.choice(responses)
    return "I'm sorry, but I don't understand."

data = load_data("patterns.json")  # Replace with your pattern data

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    response = generate_response(user_input, data)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(port=5001)
