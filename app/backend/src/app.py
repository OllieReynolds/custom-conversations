from app.common.src.mqtt import MQTTService
from config import Config
from model import ConversationModel
import random
from utils import check_cuda_available


class App():
    def __init__(self, dry_run=False):
        super().__init__()
        if not dry_run:
            self.mqtt_service = MQTTService()
            self.mqtt_service.start(True)
            self.mqtt_setup()
        
    def mqtt_setup(self):
        self.mqtt_service.subscribe("req/app/generate_conversation", self.callback_generate_conversation)
        self.mqtt_service.subscribe("req/utils/check_cuda_available", self.callback_check_cuda_available)
        
    def callback_generate_conversation(self):
        conversation = self.generate_conversation()
        self.mqtt_service.publish("rec/app/generate_conversation", conversation)
        
    def callback_check_cuda_available(self):
        cuda_available = check_cuda_available()
        self.mqtt_service.publish("rec/utils/check_cuda_available", str(cuda_available))

    def generate_conversation(self):
        config = Config()
        conversation_model = ConversationModel(config)
        with open(config.file_path, 'r', encoding='utf-8') as file:
            all_lines = file.read().splitlines()
        num_lines = 30
        random_start = random.randint(0, len(all_lines) - num_lines)
        selected_lines = all_lines[random_start:random_start + num_lines]
        conversation_history = " ".join(selected_lines)
        return conversation_model.continue_conversation(conversation_history)

if __name__ == "__main__":
    dry_run = False
    app_instance = App(dry_run)
    
    if not dry_run:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Stopping application...")
    else:
        foo = app_instance.generate_conversation()
        print (foo)

