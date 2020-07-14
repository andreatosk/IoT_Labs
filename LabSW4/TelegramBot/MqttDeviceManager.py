import json
import time
import paho.mqtt.client as mqtt

from DeviceManager import DeviceManager

class MqttDeviceManager(object):
	def __init__(self, client_id):
		self.client_id = client_id
		self.topic = '/mqtt/devices/'
		self.broker = 'test.mosquitto.org'
		self.port = 1883
		self.qos = 2
		self.client = mqtt.Client(client_id, False)
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.on_subscribe = self.on_subscribe

	def on_connect(self, paho_mqtt, userdata, flags, rc):
		self.client.subscribe(self.topic, self.qos)

	def on_message(self, paho_mqtt, userdata, msg):
		recieved_json = json.loads(msg.payload.decode())
		error, response = DeviceManager.bad_request(recieved_json)
		if error is True:
			print(response)
			return
		DeviceManager.add_from_mqtt(recieved_json)

	def on_subscribe(self, client, userdata, mid, granted_qos):
		pass

	def start(self):
		self.client.connect(self.broker, self.port)
		self.client.loop_start()

	def stop(self):
		self.client.loop_stop()
		self.client.unsubscribe(self.topic)
		self.client.disconnect()



