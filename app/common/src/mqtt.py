import paho.mqtt.client as mqtt

class MQTTService:
    def __init__(self, broker_address="broker.emqx.io", port=1883):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_address = broker_address
        self.port = port
        self.callbacks = {}

    def start(self, loop_forever=False):
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_forever() if loop_forever else self.client.loop_start()

    def subscribe(self, topic, callback):
        self.client.subscribe(topic)
        self.callbacks[topic] = callback

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print("Connected with result code " + str(reason_code))

    def on_message(self, client, userdata, msg):
        if msg.topic in self.callbacks:
            self.callbacks[msg.topic](msg.payload.decode())
