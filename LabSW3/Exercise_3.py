import paho.mqtt.client as moquette
import json
import time
import requests

class MQTTPublisher():
    def __init__(self, ID, catalogURL):
        self.ID=ID
        self.description="publisher"
        self._mqtt=moquette.Client(self.ID, False)
        self.catalogURL=catalogURL
        self.broker=None
        self.port=None
        self.topics=[]

        # assumo che il led di default sia spento
        self.__LED_ON=False

        #registro al catalogo
        success=self._register()

        if not success:
            print("Failed to register to catalog.")
            return
        # ottengo info dal catalogo:
        success=self._get_message_broker()

        if not success:
            print("Failed to retrieve Message Broker info.")
            return
        #ottengo gli endpoints dal catalogo
        success=self._get_topics()
        if not success:
            print("Failed to retrieve endpoints.")
            return

        self.start()

    def _register(self):
        myself={}
        jdict={}
        jdict['service_id']=self.ID
        jdict['description']=self.description
        jdict['endpoints']=[]
        myself[self.ID]=jdict

        try:
            r=requests.put(self.catalogURL, json.dumps(myself))
        except requests.exceptions.RequestException as e:
            #print(e)
            return False
        return True

    def _get_message_broker(self):
        try:
            r=requests.put(self.catalogURL)
        except requests.exceptions.RequestException as e:
            return False
        data=json.loads(r.content)
        self.broker=data['ip_address']
        self.port=data['port']
        return True

    def _get_topics(self):
        #la post senza parametri mi ritorna tutti i services del catalogo
        try:
            r=requests.post(self.catalogURL)
        except requests.exceptions.RequestException as e:
            return False
        services=r.content
        for s_ID, service in services.items():
            if service['description']=='led':
                for ep in service['endpoints']:
                    self.endpoints.append(json.loads(ep))

                self.topics.extend(service['endpoints'])
        return True

    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()

    def switch_LED(self, state):
        if type(state) != type(True):
            #errore: il messaggio può essere solo booleano
            return False
        if state == self.__LED_ON:
            #il comando non ha effetto: non serve neanche comunicare il messaggio al broker
            return

        #per il momento assumo che ci sia un solo topic valido
        topic=self.endpoints[0]
        #PER IL DATAFORMAT DEVO CONOSCERE CHE COSA SI ASPETTA IL CLIENT MQTT SULLA YÙN
        message={"bn":self.ID,
                "e":[
                {
                    "n":"led",
                    "t":time.time(),
                    "v":int(state),
                    "u":None
                }
            ]
        }
        self.__LED_ON=state
        self._mqtt.publish(topic, json.dumps(message),2)

def main():
    client=MQTTPublisher('myid', 'http://localhost')

if __name__ == '__main__':
    main()