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

        # assumo che il led di default sia spento
        self.__LED_ON=False

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
        jdict={}
        jdict['service_id']=self.ID
        jdict['description']=self._description
        jdict['endpoints']=[]
        myself[self.ID]=jdict

        r=requests.put(catalogURL, json.dumps(myself))
        if not r:
            #4xx o 5xx
            return False
        return True

    def _get_message_broker(self):
        r=requests.get(catalogURL)
        if not r:
            #vuol dire che è stato ritornato un errore 4xx o 5xx
            return False
        data=json.loads(r.content)
        self.broker=data['ip_address']
        self.port=data['port']
        return True

    def _get_topics(self):
        #la post senza parametri mi ritorna tutti i services del catalogo
        r=requests.post(self.catalogURL)
        if not r:
            #4xx o 5xx
            return False
        services=r.content
        for s_ID, service in services.items():
            if service['description']=='led'
                self.topics.extend(service['endpoints'])
        return True

    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()

    def switch_LED(self, state):
        if type(state) != type(True):
            #errore: il messaggio può essere solo booleano
            pass
        if state == self.__LED_ON:
            #il comando non ha effetto: non serve neanche comunicare il messaggio al broker
            return
        #Quale topic scelgo tra quelli validi dello Yùn?
        topic=''
        #PER IL DATAFORMAT DEVO CONOSCERE CHE COSA SI ASPETTA IL CLIENT MQTT SULLA YÙN
        self._mqtt.publish(topic, data,2)
