import paho.mqtt.client as mqtt
import time
import json

class DevicePublisher(object):
	def __init__(self, client_id):
		self.client_id = client_id

		self.client = mqtt.Client(self.client_id, False)
		self.client.on_connect = self.on_connect
		self.broker = '192.168.1.16'
		self.port = 8080
		self.topic = '/mqtt/devices/'

	def on_connect(self):
		print('Connected')

	def start(self):
		self.client.connect(self.broker, self.port)
		self.client.loop_start()

	def stop(self):
		self.client.loop_stop()
		self.client.disconnect()

	def publish(self, topic):
		msg = {}
		device_id = 'random_device_id'
		msg['device_id'] = {}
		msg['device_id']['device_id'] = device_id
		msg['endpoints'] = []
		msg['resources'] = []
		msg['endpoints'].append('random_endpoint')
		msg['resources'].append('random_resource')

		self.client.publish(topic, json.dumps(msg), 2)

if __name__ == '__main__':
	publisher = DevicePublisher('random_publisher_id')
	publisher.start()

	for i in range(10):
		print('Publish #'+str(i+1))
		publisher.publish(publisher.topic)
		time.sleep(1)

	publisher.stop()