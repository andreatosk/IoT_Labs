import paho.mqtt.client as moquette
import json

class MQTTPublisher():
    def __init__(self, ID, catalogURL):
        self.ID=ID
        self.description="publisher"
        self._mqtt=moquette.Client(self.ID, False)
        self._mqtt.on_message=self.on_message
        self.catalogURL=catalogURL
        self.broker=None
        self.port=None
        self.topics={}

        #registro al catalogo
        success=self._register()

        if not success:
            return("Failed to register to catalog.")
        # ottengo info dal catalogo:
        success=self._get_message_broker()

        if not success:
            return("Failed to retrieve Message Broker info.")
        #ottengo gli endpoints dal catalogo
        success=self._get_topics()
        if not success:
            return("Failed to retrieve endpoints.")

        self.start()

    def _register(self):
        myself={}
        myself['service_id']=self.ID
        myself['description']=self._description
        myself['endpoints']=[]

        r=requests.put(catalogURL, json.dumps(myself))
        if not r:
            return False
        return True

    def _get_message_broker(self):
        r=requests.get(catalogURL)
        if not r:
            return False
        data=json.loads(r.content)
        self.broker=data['ip_address']
        self.port=data['port']
        return True

    def _get_topics(self):
        #la post senza parametri mi ritorna tutti i services del catalogo
        r=requests.post(self.catalogURL)
        if not r:
            return False
        services=r.content
        for s_ID, service in services.items():
            #NON DOVREBBERO ESSERE TUTTI I TOPIC (?)
            self.topics[service['description']]=service['endpoints']
        return True

    def _publish(self, topic, payload):
        pass

    def _subscribe(self, topic):
        if not self.__isSub:
            self._mqtt.subscribe(topic, qos=2)
            self.__isSub=True

    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()

    def on_message(self, client, userdata, msg):
        pass


    #punto 1
    def actuate_fan(self):
        pass

    #punto 2
    def actuate_led(self):
        pass

    #punto 5
    def sense_people(self):
        #riceve info da PIR e noise
        pass

    #punti 3 e 4 implementati nel 5
    #punto 6 non necessario

    #punto 8
    def change_set_points(self, min_fan=None, max_fan=None, min_led=None, max_led=None):
        #cambia solo i setpoint effettivamente ricevuti
        #NB: PASSARE I PARAMETRI NELLA FORMA KEY=VALUE
        pass
