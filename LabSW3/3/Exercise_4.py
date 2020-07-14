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
        jdict={}
        jdict['service_id']=self.ID
        jdict['description']=self._description
        jdict['endpoints']=[]
        myself[self.ID]=jdict

        try:
            r=requests.put(catalogURL, json.dumps(myself))
        except requests.exceptions.RequestException as e:
            return False
        return True

    def _get_message_broker(self):
        try:
            r=requests.get(catalogURL)
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
            #NON DOVREBBERO ESSERE TUTTI GLI ENDPOINTS (?)
            key=service['description']
            self.topics[key]=[]
            for ep in service['endpoints']:
                self.topics.append(json.loads(ep))
            
        return True

    def _publish(self, topic, payload):
        self._mqtt.publish(topic, payload, qos=2)

    def _subscribe(self, topic):
        if not self.__isSub:
            self._mqtt.subscribe(topic, qos=2)
            self.__isSub=True

    def start(self):
        self._mqtt.connect(self.broker, self.port)
        self._mqtt.loop_start()

    def on_message(self, client, userdata, msg):
        if msg.topic.split('/')[-1]=='people':
            self.sense_people(msg.payload)

    #punto 1
    def actuate_fan(self, value):
        #TODO: sistemare le chiavi 
        topic=self.topics['fan'][]
        value=int(value)
        if value <0 or value >255:
            return False
        message={"bn":self.ID,
                "e":[
                {
                    "n":"fan",
                    "t":time.time()
                    "v":value,
                    "u":None
                }
            ]
        }
        self._publish(topic, json.dumps(message))
        return True

    #punto 2
    def actuate_led(self, value):
        topic=self.topics['led'][]
        value=int(value)
        if value <0 or value >255:
            return False
        message={"bn":self.ID,
                "e":[
                {
                    "n":"led",
                    "t":time.time()
                    "v":value,
                    "u":None
                }
            ]
        }
        self._publish(topic, json.dumps(message))
        return True

    #punto 5
    def sense_people(self, payload):
        #riceve info da PIR e noise
        message=json.loads(payload)
        num_people=message['e']['v']
        #CHE FACCIO CON IL NUMERO DI PERSONE?
        

    #punti 3 e 4 implementati nel 5
    #punto 6 non necessario

    #punto 8
    def change_set_points(self, min_fan=None, max_fan=None, min_led=None, max_led=None):
        #cambia solo i setpoint effettivamente ricevuti
        #NB: PASSARE I PARAMETRI NELLA FORMA KEY=VALUE PER EVITARE DI RISPETTARE L'ORDINE DEI PARAMETRI
        topic=self.topics['setpoints'][]
        if min_fan not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time()
                        "v":min_fan,
                        "u":None
                    }   
                ]
            }
            self._publish(topic, json.dumps(message))
        if max_fan not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time()
                        "v":max_fan,
                        "u":None
                    }   
                ]
            }
            self._publish(topic, json.dumps(message))
        if min_led not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time()
                        "v":min_led,
                        "u":None
                    }   
                ]
            }
            self._publish(topic, json.dumps(message))
        if max_led not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time()
                        "v":max_led,
                        "u":None
                    }   
                ]
            }
            self._publish(topic, json.dumps(message))

