from MQTT import Moquette
import json
import requests

class MQTTPublisher():
    def __init__(self, ID, catalogURL):
        self.ID=ID
        self.description="publisher"
        self.catalogURL=catalogURL
        self.broker=None
        self.port=None
        self.topics={}
        self.__useful_topics=['fan','led','people','heating','setpoints']

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

        self._mqtt=Moquette(self.ID, self.broker, self.port, self, self.topics)
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
            raise e

    def _get_message_broker(self):
        try:
            r=requests.get(self.catalogURL)
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
            #NON DOVREBBERO ESSERE TUTTI GLI ENDPOINTS (?)

            eps=[]
            for ep in service['endpoints']:
                eps.append(json.loads(ep))
            for ep in eps:
                if ep['description'] in self.__useful_topics:
                    self.topics[ep['description']]=ep['value']
            
    def start(self):
        self._mqtt.start()

    def stop(self):
        self._mqtt.stop()


    #punto 1
    def actuate_fan(self, value):
        #TODO: sistemare le chiavi 
        value=int(value)
        if value <0 or value >255:
            return False
        message={"bn":self.ID,
                "e":[
                {
                    "n":"fan",
                    "t":time.time(),
                    "v":value,
                    "u":None
                }
            ]
        }
        self._mqtt.publish('fan',json.dumps(message))
        return True

    #punto 2
    def actuate_heating(self, value):
        value=int(value)
        if value <0 or value >255:
            return False
        message={"bn":self.ID,
                "e":[
                {
                    "n":"heating",
                    "t":time.time(),
                    "v":value,
                    "u":None
                }
            ]
        }
        self._mqtt.publish('heating', json.dumps(message))
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
        #cambia solo i setpoint effettivamente ricevuti come parametri
        if min_fan is not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time(),
                        "v":min_fan,
                        "u":None
                    }   
                ]
            }
            self._mqtt.publish('setpoints', json.dumps(message))
        if max_fan is not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time(),
                        "v":max_fan,
                        "u":None
                    }   
                ]
            }
            self._mqtt.publish('setpoints', json.dumps(message))
        if min_led is not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time(),
                        "v":min_led,
                        "u":None
                    }   
                ]
            }
            self._mqtt.publish('setpoints', json.dumps(message))
        if max_led is not None:
            message={"bn":self.ID,
                    "e":[
                    {
                        "n":"led",
                        "t":time.time(),
                        "v":max_led,
                        "u":None
                    }   
                ]
            }
            self._mqtt.publish('setpoints', json.dumps(message))


def main():
    client=MQTTPublisher('myID','http://localhost')
    print(client)

if __name__ == '__main__':
    main()