import paho.mqtt.client as moquette

class Moquette:
    """Moquette: a general purpose MQTT client"""
    def __init__(self, broker, port, notifier):
        self.broker=broker
        self.port=port
        self.notifier=notifier

        self.mqtt=Client(self.broker, self.port)
        self.mqtt.on_message=self.on_message
        self.mqtt.on_connect=self.on_connect

    def start(self):
        pass

    def stop(self):
        pass


    def on_message(self, client, userdata, msg):
        pass
