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

        #registro al catalogo
        self._register()
        # ottengo info dal catalogo:
        self._get_message_broker()

        #ottengo gli endpoints dal catalogo
        self._get_topics()

        self.start()

    def _register(self):
        myself={}
        myself['service_id']=self.ID
        myself['description']=self._description
        myself['endpoints']=[]

        r=requests.put(catalogURL, json.dumps(myself))
        if not r:
            #4xx o 5xx
            pass

    def _get_message_broker(self):
        r=requests.get(catalogURL)
        if not r:
            #vuol dire che è stato ritornato un errore 4xx o 5xx
            pass
        data=json.loads(r.content)
        self.broker=data['ip_address']
        self.port=data['port']

    def _get_topics(self):
        #la post senza parametri mi ritorna tutti i services del catalogo
        r=requests.post(self.catalogURL)
        if not r:
            #4xx o 5xx
        services=r.content
        for s_ID, service in services.items():
            #NON DOVREBBERO ESSERE TUTTI I TOPIC
            self.topics.extend(service['endpoints'])

    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()

    def actuate_fan(self):
        pass

    def actuate_led(self):
        pass

    def sense_people(self):
        #riceve info da PIR e noise
        pass

    #punti 3 e 4 implementati nel 5
    #punto 6 non necessario

    def change_set_points(self, min_fan=None, max_fan=None, min_led=None, max_led=None):
        #cambia solo i setpoint effettivamente ricevuti
        #NB: PASSARE I PARAMETRI NELLA FORMA KEY=VALUE
        pass
