import json
import time
import paho.mqtt.client as mqtt
import DeviceManager

registered_devices = {}
registered_devices_filename = 'devices.json' # Dovrebbe cooperare con le API Rest? Errori di divergenza dei dati?

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
		self.topic = '/mqtt/devices/'
		self.broker = 'test.mosquitto.org'
		self.port = 1883
		self.qos = 2
		self.client = mqtt.Client(client_id, False)
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.on_log = self.on_log 	#For Debug Purposes Only
		self.client.on_subscribe = self.on_subscribe

	def on_connect(self, paho_mqtt, userdata, flags, rc):
		self.client.subscribe(self.topic, self.qos)

	def on_message(self, paho_mqtt, userdata, msg):
		recieved_json = json.loads(msg.payload.decode())
		error, response = DeviceManager.bad_request(recieved_json)
		if error is True:
			print(response)
			return
		if recieved_json['device_id'] not in registered_devices.keys():
			new_device = DeviceManager.format_new_device(recieved_json)
			registered_devices[new_device['device_id']] = new_device
		else:
			registered_devices[recieved_json['device_id']]['insertion_timestamp'] = str(time.time())

			
		DeviceManager.add_from_mqtt(recieved_json)

	def on_subscribe(self, client, userdata, mid, granted_qos):
		pass

	# For Debug Purposes Only
	def on_log(self, paho_mqtt, userdata, level, buf):
		print('[LOG] : ' + buf)

	def start(self):
		self.client.connect(self.broker, self.port)
		self.client.loop_start()


	def stop(self):
		self.client.loop_stop()
		self.client.unsubscribe(self.topic)
		self.client.disconnect()



