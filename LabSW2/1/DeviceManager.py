import cherrypy
import json
import time

registered_devices = {}
registered_devices_filename = 'devices.json'

class DeviceManager(object):
	

	def __init___(self):
		global registered_devices, registered_devices_filename
		registered_devices = json.load(registered_devices_filename)


	def bad_request(recieved_json):
		if len(recieved_json) != 4:
			return True, 'Incorrect number of arguments'
		for argument in recieved_json:
			if len(argument) < 1:
				return True, 'Invalid arguments'
		if not isinstance(recieved_json['resources'], list):
			return True, '"resources" field has to be an array/list'
		for resource in recieved_json['resources']:
			if len(resource) < 1:
				return True, "Invalid resource(s)"
		if not isinstance(recieved_json['insertion_timestamp'], str):
			return True, '"insertion_timestamp" has to be a string'
		global registered_services
		if recieved_json['device_id'] in registered_services.keys():
			return True, 'device_id already exists'
		return False, ''


	@cherrypy.expose
	@cherrypy.tools.json_in()
	def PUT(self):
		global registered_devices
		recieved_json = cherrypy.request.json
		new_device = {}
		new_device['device_id'] = recieved_json['device_id']
		new_device['resources'] = []
		for resource in recievied_json['resources']:
			with new_device['resources'] as resources:
				resources.append(recievied_json[resource])
		new_device['insertion_timestamp'] = str(time.time())
		registered_devices['device_id'] = new_device
		json.dump(registered_devices, registered_devices_filename)

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def GET(self):
		# Se 'device_id' è vuoto, ritorna tutto
		# Se 'device_id' contiene un id, ritorna quello
		global registered_devices
		recievied_json = cherrypy.request.json
		request = recievied_json['device_id']
		if request == '':
			return json.dumps(registered_devices)
		else:
			return json.dumps(registered_devices[request])

	@cherrypy.expose
	def POST(self):
		cherrypy.response.status = 403
		return "Error"

	@cherrypy.expose
	def DELETE(self):
		cherrypy.response.status = 403
		return "Error"
	