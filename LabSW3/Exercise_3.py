import paho.mqtt.client as moquette
import json

class MQTTPublisher():
    def __init__(self, ID, catalog):
        self.ID=ID

        self._mqtt=moquette.Client(self.ID, False)
        self._mqtt.on_message=self.on_message

        # assumo che il led di default sia spento
        self.__LED_ON=False

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

    def switch_LED(self, state):
        if type(state) != type(True):
            #errore: il messaggio può essere solo booleano
        self._mqtt.publish()
