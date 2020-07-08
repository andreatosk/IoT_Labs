import cherrypy
import json
import time

registered_devices = {}
registered_devices_filename = 'devices.json'

class DeviceManager(object):
	exposed = True
	file_locked = False
	memory_locked = False

	def __init__(self):
		global registered_devices, registered_devices_filename
		try:
			with open(registered_devices_filename, 'r') as file:
				registered_devices = json.load(file)
				file.close()
		except:
			pass # JSON vuoti

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
		

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def PUT(self):
		global registered_devices
		recieved_json = cherrypy.request.json


		error, response = DeviceManager.bad_request(recieved_json)
		if error is True:
			cherrypy.response.status = 400
			return response

		DeviceManager.get_memory_access()
		if recieved_json['device_id'] not in registered_devices.keys():
			new_device = DeviceManager.format_new_device(recieved_json)
			registered_devices[new_device['device_id']] = new_device
		else:
			registered_devices[recieved_json['device_id']]['insertion_timestamp'] = str(time.time())
		DeviceManager.unlock_memory()
		DeviceManager.write_to_local()

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def POST(self):
		# Se 'device_id' è vuoto, ritorna tutto
		# Se 'device_id' contiene un id, ritorna quello
		global registered_devices
		recievied_json = cherrypy.request.json
		request = recievied_json['device_id']
		if request == '':
			return json.dumps(registered_devices)
		else:
			try:
				return json.dumps(registered_devices[request])
			except:
				return json.dumps({})

	def write_to_local():
		global registered_devices
		DeviceManager.get_file_access()
		with open(registered_devices_filename, 'w') as file:
			json.dump(registered_devices, file)
			file.close()
		DeviceManager.unlock_file()

	def add_from_mqtt(recieved_json):
		global registered_devices
		global registered_devices_filename
		DeviceManager.get_memory_access()
		DeviceManager.get_file_access()
		registered_devices[recieved_json['device_id']] = recieved_json
		DeviceManager.write_to_local()
		DeviceManager.unlock_file()
		DeviceManager.unlock_memory()


	def get_memory_status():
		return DeviceManager.memory_locked

	def get_file_status():
		return DeviceManager.file_locked

	def lock_memory():
		DeviceManager.memory_locked = True

	def get_memory_access():
		while DeviceManager.get_memory_status() is True:
			pass
		DeviceManager.lock_memory()

	def get_file_access():
		while DeviceManager.get_file_status() is True:
			pass
		DeviceManager.lock_file()

	def lock_file():
		DeviceManager.file_locked = True

	def unlock_file():
		DeviceManager.file_locked = False

	def unlock_memory():
		DeviceManager.memory_locked = False

	def get_mem_json():
		global registered_devices
		return registered_devices

	def get_filename():
		global registered_devices_filename
		return registered_devices_filename

	def set_mem_json(json):
		global registered_devices
		registered_devices = json