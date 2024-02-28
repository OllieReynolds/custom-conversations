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

@app.route('/generate_conversation', methods=['POST'])
def generate_conversation():
    if request.content_type != 'text/plain':
        return jsonify(error="Unsupported Media Type. Please send text/plain content."), 415

    raw_text = request.data.decode('utf-8')
    if not raw_text:
        return jsonify(error="No text provided"), 400

    config = config_manager.get_config()
    chat_model = ChatModel(config)
    try:
        conversation = chat_model.generate_reply(raw_text)
    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(conversation=conversation)

@app.route('/train', methods=['POST'])
def train_model():
    use_sample = request.args.get('use_sample') == 'true'
    if use_sample:
        temp_training_file = "app/backend/input/sample.txt"
    else:
        if request.content_type != 'text/plain':
            return jsonify(error="Unsupported Media Type. Please send text/plain content."), 415

        raw_text = request.data.decode('utf-8')
        if not raw_text:
            return jsonify(error="No text provided"), 400

        temp_training_file = "app/backend/input/temp_training_data.txt"
        with open(temp_training_file, "w") as file:
            file.write(raw_text)

    try:
        config = config_manager.get_config()
        chat_model = ChatModel(config)
        chat_model.retrain_model(temp_training_file)
    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(success=True, message="Model retrained successfully")

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
