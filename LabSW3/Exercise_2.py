import paho.mqtt.client as moquette
import json
import requests

class MQTTSubscriber():
    def __init__(self, ID, catalogURL):
        self._ID=ID
        self._description='subscriber'
        self.catalogURL=catalogURL
        self.broker=None
        self.port=None
        self.__paths=[]
        self.topics={}

        self._mqtt=moquette.Client(self.ID, False)
        self._mqtt.on_message=self.on_message


        #registro al catalogo
        self._register()        

        #ricavo le info sul broker
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
        r=requests.get(self.catalogURL)
        if not r:
            #vuol dire che è stato ritornato un errore 4xx o 5xx
            pass
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
        r=requests.post(self.catalogURL)
        if not r:
            #4xx o 5xx
        services=r.content
        for s_ID, service in services.items():
            if service['description']=='temperature'
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