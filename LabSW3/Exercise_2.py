import paho.mqtt.client as moquette
import json
import requests

class MQTTSubscriber():
    def __init__(self, ID, catalogURL):
        self.ID=ID
        self.description='subscriber'
        self.catalogURL=catalogURL
        self.broker=None
        self.port=None
        self.__paths=[]
        self.topics={}

        self._mqtt=moquette.Client(self.ID, False)
        self._mqtt.on_message=self.on_message

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
            r=requests.get(self.catalogURL)
        except requests.exceptions.RequestException as e:
            raise e
        data=json.loads(r.content)
        self.broker=data['ip_address']
        self.port=data['port']
        self.broker['endpoints']=data['endpoints']
        #broker['endpoints']:
        # - [0]:/devices
        # - [1]:/users
        # - [2]:/services

    def _get_topics(self):
        #la post senza parametri mi ritorna tutti i services del catalogo
        try:
            r=requests.post(self.catalogURL)
        except requests.exceptions.RequestException as e:
            raise e
        services=r.content
        for s_ID, service in services.items():
            if service['description']=='temperature':
                self.topics.extend(service['endpoints'])


    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()
        self.subscribe()

    def subscribe(self):
        tuples=[]
        for topic in self.topics:
            tuples.append((topic, 2))
        self._mqtt.subscribe(tuples)


    def on_message(self, client, userdata, msg):
        data=json.loads(msg.payload)
        print(f"Received data from {data['bn']}:")
        print(f"{data['e']['n']}: {data['e']['v']:.3}{data['e']['u']}")


def main():
    client=MQTTSubscriber('myID', 'http://0.0.0.0')


if __name__ == '__main__':
    main()