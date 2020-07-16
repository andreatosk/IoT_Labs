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

        try:
            self._register()
        except Exception as e:
            #print("Failed to register to catalog.")
            raise e

        # ottengo info dal catalogo:
        try:
            self._get_message_broker()
        except Exception as e:
            #print("Failed to retrieve Message Broker info.")
            raise e

        #ottengo gli endpoints dal catalogo
        try:
            self._get_topics()
        except Exception as e:
            #print("Failed to retrieve endpoints.")
            raise e

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
            raise e


    def _get_message_broker(self):
        try:
            r=requests.put(self.catalogURL)
        except requests.exceptions.RequestException as e:
            raise e
        data=json.loads(r.content)
        self.broker=data['ip_address']
        self.port=data['port']

    def _get_topics(self):
        #la post senza parametri mi ritorna tutti i services del catalogo
        try:
            r=requests.post(self.catalogURL)
        except requests.exceptions.RequestException as e:
            raise e
        services=r.content
        for s_ID, service in services.items():

            eps=[]
            for ep in service['endpoints']:
                eps.append(json.loads(ep))
            for ep in eps:
                if ep['description'] == 'led' :
                    #ASSUMO CHE CI SIA UN UNICO ENDPOINT UTILE
                    self.topic=ep.value
                    break

    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()

    def switch_LED(self, state):
        if type(state) != type(True):
            #errore: state può essere solo booleano
            return False
        if state == self.__LED_ON:
            #il comando non ha effetto: non serve neanche comunicare il messaggio al broker
            return

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
        self._mqtt.publish(self.topic, json.dumps(message),2)

def main():
    client=MQTTPublisher('myid', 'http://localhost')

if __name__ == '__main__':
    main()