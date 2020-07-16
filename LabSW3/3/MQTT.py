import paho.mqtt.client as moquette

class Moquette:
    """Moquette: a general purpose MQTT client"""
    def __init__(self, ID, broker, port, notifier, topics):
        self.ID=ID
        self.broker=broker
        self.port=port
        self.notifier=notifier
        self.__topics=topics

        self.__mqtt=Client(self.ID, False)
        self.__mqtt.on_message=self.on_message
        self.__mqtt.on_connect=self.on_connect

        self.__is_sub={}
        for descr, topic in self.__topics.items():
            self.__is_sub[descr]=False

    def start(self):
        self.__mqtt.connect(self.broker, self.port)
        self.__mqtt.loop_start()

    def stop(self):
        for key, value in self.__is_sub.items():
            if value:
                self._unsubscribe(key)
        self.__mqtt.loop_stop()
        self.disconnect()

    def publish(self, descr, data):
        self.__mqtt.publish(self.__topics[descr], data, qos=2)

    def subscribe(self, descr):
        self.__mqtt.subscribe(self.__topics[descr], qos=2)
        self.__is_sub[descr]=True

    def _unsubscribe(self, descr):
        if self.__is_sub[descr]:
            self.__mqtt._unsubscribe(self.__topics[descr])


    def on_message(self, client, userdata, msg):
        self.notifier.sense_people(msg.payload)

    def on_connect(self, client, userdata, flags, rc):
        pass