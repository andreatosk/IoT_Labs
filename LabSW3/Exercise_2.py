import paho.mqtt.client as moquette
import json

class MQTTSubscriber():
    def __init__(self, ID, catalog):
        self.ID=ID

        self._mqtt=moquette.Client(self.ID, False)
        self._mqtt.on_message=self.on_message

        #registro al catalogo

        # ottengo info dal catalogo:
        self.broker=broker
        self.port=port

        #ottengo gli endpoints dal catalogo
        self.topics=topics

        self.start()

    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()

    def on_message(self, client, userdata, msg):
        data=json.loads(msg.payload)
        print(f"Received data from {data['bn']}:")
        print(f"{data['e']['n']}: {data['e']['v']:.3}{data['e']['u']}")
