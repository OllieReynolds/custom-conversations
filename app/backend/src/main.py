from typing import Any
from flask import Flask, jsonify, request
from app.backend.src.ai.model import ChatModel
import random
from app.backend.src.utils.config import ConfigManager
from app.backend.src.utils.utils import check_cuda_available
from app.backend.src.utils.database import Database

app = Flask(__name__)
db = Database()
config_manager = ConfigManager(db)

@app.route('/generate_conversation', methods=['GET'])
def generate_conversation():
    config = config_manager.get_config()
    chat_model = ChatModel(config)
    try:
        with open(config.file_path, 'r', encoding='utf-8') as file:
            all_lines = file.read().splitlines()
        selected_lines = random.sample(all_lines, 30)
        conversation_history = " ".join(selected_lines)
        conversation = chat_model.generate_reply(conversation_history)
    except Exception as e:
        return jsonify(error=str(e)), 500
    return jsonify(conversation=conversation)

@app.route('/check_cuda_available', methods=['GET'])
def check_cuda_available_route():
    cuda_available = check_cuda_available()
    return jsonify(cuda_available=cuda_available)

@app.route('/config', methods=['POST'])
def update_config():
    config_data: Any | None = request.json
    if config_data:
        for key, value in config_data.items():
            config_manager.update_config(key, value)
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="No data provided"), 400
    
@app.route('/config', methods=['GET'])
def get_config_route():
    config_dict = config_manager.get_all_config_values()
    return jsonify(config_dict)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
