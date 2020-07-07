import json
import time

import paho.mqtt.client as mqtt
registered_devices = {}
registered_devices_filename = 'devices_mqtt.json' # Dovrebbe cooperare con le API Rest? Errori di divergenza dei dati?

class MqttDeviceManager(object):
	exposed=True

	def __init__(self, client_id):
		global registered_devices, registered_devices_filename
		try:
			with open(registered_devices_filename, 'r') as file:
				registered_devices = json.load(file)
		except:
			pass # JSON vuoti

		self.client_id = client_id
		self.topic = '/mqtt/devices'
		self.broker = '192.168.1.16'
		self.port = 8080
		#self.broker = 'iot.eclipse.org'

		self.client = mqtt.Client(client_id, False)
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_recieve

# Questa funzione implementa alcuni controlli basilari sul JSON ricevuto
	def bad_request(recieved_json):
		if len(recieved_json) != 3:
			return True, 'Incorrect number of arguments'

		for argument in recieved_json:
			if len(argument) < 1:
				return True, 'Invalid arguments'
		try:		
			if not isinstance(recieved_json['resources'], list):
				return True, '"resources" field has to be an array/list'
			for resource in recieved_json['resources']:
				if len(resource) < 1:
					return True, "Invalid resource(s)"
		except:
			return True, 'Missing "resources" field'

		try:
			if not isinstance(recieved_json['endpoints'], list):
				return True, '"endpoints" field has to be an array/list'
			if len(recieved_json['endpoints']) != len(recieved_json['resources']):
				return True, '"endpoints" and "resources" sizes must match'
		except:
			return True, 'Missing "endpoints" field'

		try:
			test = recieved_json['device_id']
		except:
			return True, 'Missing "device_id" field'

		return False, ''


	def format_new_device(recieved_json):	
		new_device = {}
		new_device['device_id'] = recieved_json['device_id']
		new_device['resources'] = []
		for resource in recieved_json['resources']:
			new_device['resources'].append(resource)
		new_device['endpoints'] = []
		for endpoint in recieved_json['endpoints']:
			new_device['endpoints'].append(endpoint)
		new_device['insertion_timestamp'] = str(time.time())
		return new_device


	def write_to_local():
		global registered_devices
		with open(registered_devices_filename, 'w') as file:
			json.dump(registered_devices, file)

	def on_connect(self, paho_mqtt, userdata, flags, rc):
		# For Debug Only
		print("Successfully Connected")

	def on_recieve(self, paho_mqtt, userdata, msg):
		error, response = bad_request(userdata)
		if error is True:
			print('Recieved a bad message!')
			return
		print('Paho Recieved a good message!')
		if recieved_json['device_id'] not in registered_devices.keys():
			new_device = DeviceManager.format_new_device(recieved_json)
			registered_devices[new_device['device_id']] = new_device
		else:
			registered_devices[recieved_json['device_id']]['insertion_timestamp'] = str(time.time())
			
		MqttDeviceManager.write_to_local()

	def start(self):
		self.client.connect(self.broker, self.port)
		print('Paho Connected')
		self.client.subscribe(self.topic, 2)
		print('Paho Subscribed.')
		self.client.loop_start()
		print('Paho Started Looping')

	def stop(self):
		self.client.loop_stop()
		print('Paho Stopped Looping')
		self.client.unsubscribe(self.topic)
		print('Paho Unsubscribed from ' + self.topic)
		self.client.disconnect()
		print('Paho Disconnected')

