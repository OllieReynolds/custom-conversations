from flask import Flask, jsonify
from config import Config
from model import ConversationModel
import random
from utils import check_cuda_available

app = Flask(__name__)

@app.route('/generate_conversation', methods=['GET'])
def generate_conversation():
    config = Config()
    conversation_model = ConversationModel(config)
    with open(config.file_path, 'r', encoding='utf-8') as file:
        all_lines = file.read().splitlines()
    num_lines = 30
    random_start = random.randint(0, len(all_lines) - num_lines)
    selected_lines = all_lines[random_start:random_start + num_lines]
    conversation_history = " ".join(selected_lines)
    conversation = conversation_model.continue_conversation(conversation_history)
    return jsonify(conversation=conversation)

@app.route('/check_cuda_available', methods=['GET'])
def check_cuda_available_route():
    cuda_available = check_cuda_available()
    return jsonify(cuda_available=cuda_available)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
