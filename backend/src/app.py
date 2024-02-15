from config import Config
from data_loader import DataLoader
from model import ConversationModel
import random
import os

def generate_conversation():
    config = Config()
    conversation_model = ConversationModel(config)
    all_lines = DataLoader.load_conversation_data(config.file_path)
    num_lines = 30
    random_start = random.randint(0, len(all_lines) - num_lines)
    selected_lines = all_lines[random_start:random_start + num_lines]
    conversation_history = " ".join(selected_lines)
    return conversation_model.continue_conversation(conversation_history)

# Uncomment the following lines if you want to run this as a script
if __name__ == "__main__":
    print(generate_conversation())
