from config import Config
from model import ConversationModel
import random
import paho.mqtt.client as mqtt
import threading
from utils import check_cuda_available

class App():
    def __init__(self, dry_run=False):
        super().__init__()
        if not dry_run:
            self.mqtt_setup()
        
    def mqtt_setup(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.loop_forever()
        
    def on_connect(self, client, userdata, flags, reason_code, properties):
        print("Connected with result code " + str(reason_code))
        self.client.subscribe("req/app/generate_conversation")
        self.client.subscribe("req/utils/check_cuda_available")
        
    def on_message(self, client, userdata, msg):
        if msg.topic == "req/app/generate_conversation":
            threading.Thread(target=self.generate_conversation_and_publish).start()
        elif msg.topic == "req/utils/check_cuda_available":
            cuda_available = check_cuda_available()
            self.client.publish("rec/utils/check_cuda_available", str(cuda_available))
            
    def generate_conversation_and_publish(self):
        conversation = self.generate_conversation()
        self.client.publish("rec/app/generate_conversation", conversation)

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

