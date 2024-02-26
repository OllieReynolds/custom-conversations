from flask import Flask, jsonify, request
from app.backend.src.database import get_config_value, set_config_value
from config import load_config
from model import ConversationModel
import random
from utils import check_cuda_available

app = Flask(__name__)
config = load_config()

def load_or_initialize_db_config():
    db_config_keys = [
        'model_directory', 'model_name', 'model_type', 'num_train_epochs',
        'per_device_train_batch_size', 'gradient_accumulation_steps', 'fp16',
        'learning_rate', 'warmup_steps', 'save_steps', 'save_total_limit',
        'evaluation_strategy', 'eval_steps', 'use_early_stopping', 'early_stopping_patience',
        'use_lr_scheduler', 'lr_scheduler_type', 'logging_dir', 'logging_steps',
        'do_train', 'do_eval', 'do_predict', 'load_best_model_at_end', 'metric_for_best_model',
        'greater_is_better', 'file_path', 'device', 'max_length_increment', 'do_sample',
        'top_k', 'no_repeat_ngram_size', 'temperature', 'top_p'
    ]
    for key in db_config_keys:
        value = get_config_value(key)
        if value is None:
            default_value = getattr(config, key, None)
            set_config_value(key, default_value)

load_or_initialize_db_config()

@app.route('/generate_conversation', methods=['GET'])
def generate_conversation():
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

@app.route('/config', methods=['POST'])
def update_config():
    config_data = request.json
    for key, value in config_data.items():
        set_config_value(key, value)
        if hasattr(config, key):
            setattr(config, key, value)
    return jsonify(success=True)

@app.route('/config', methods=['GET'])
def get_config_route():
    config_attrs = [
        'model_directory', 'model_name', 'model_type', 'num_train_epochs',
        'per_device_train_batch_size', 'gradient_accumulation_steps', 'fp16',
        'learning_rate', 'warmup_steps', 'save_steps', 'save_total_limit',
        'evaluation_strategy', 'eval_steps', 'use_early_stopping', 'early_stopping_patience',
        'use_lr_scheduler', 'lr_scheduler_type', 'logging_dir', 'logging_steps',
        'do_train', 'do_eval', 'do_predict', 'load_best_model_at_end', 'metric_for_best_model',
        'greater_is_better', 'file_path', 'device', 'max_length_increment', 'do_sample',
        'top_k', 'no_repeat_ngram_size', 'temperature', 'top_p'
    ]
    config_dict = {attr: getattr(config, attr, None) for attr in config_attrs}
    return jsonify(config_dict)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
