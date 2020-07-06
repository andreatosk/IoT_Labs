import cherrypy
import json
import time

registered_services = {}
registered_services_filename = 'services.json'

class ServiceManager(object):
	exposed = True

	def __init__(self):
		global registered_services, registered_services_filename
		try:
			with open(registered_services_filename, 'r') as file:
				registered_services = json.load(file)
		except:
			pass # JSON vuoti
		self.exposed = True


	def bad_request(recieved_json):
		if len(recieved_json) != 3:
			return True, 'Incorrect number of arguments'
		for argument in recieved_json:
			if len(argument) < 1:
				return True, 'Invalid arguments'
		if not isinstance(recieved_json['endpoints'], list):
			return True, '"endpoints" field has to be an array/list'
		for endpoint in recieved_json['endpoints']:
			if len(endpoint) < 1:
				return True, "Invalid endpoint(s)"
		global registered_services
		return False, ''


	def format_new_service(recieved_json):
		new_service = {}
		new_service['service_id'] = recieved_json['service_id']
		new_service['description'] = recieved_json['description']
		new_service['endpoints'] = []
		for endpoint in recieved_json['endpoints']:
			new_service['endpoints'].append(endpoint)
		new_service['insertion_timestamp'] = str(time.time())

		return new_service

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def PUT(self):
		global registered_services
		recieved_json = cherrypy.request.json

		error, response = ServiceManager.bad_request(recieved_json)
		if error is True:
			cherrypy.response.status = 400
			return response

		if recieved_json['service_id'] not in registered_services:
			new_service = ServiceManager.format_new_service(recieved_json)
			registered_services[recieved_json['service_id']] = new_service
		else:
			registered_services['service_id']['insertion_timestamp'] = str(time.time())
		

		with open(registered_services_filename, 'w') as file:
			json.dump(registered_services, file)

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def POST(self):
		# Se 'service_id' è vuoto, ritorna tutto
		# Se 'service_id' contiene un id, ritorna quello
		global registered_services
		recievied_json = cherrypy.request.json
		request = recievied_json['service_id']
		if request == '':
			return json.dumps(registered_services)
		else:
			try:
				return json.dumps(registered_services[request])
			except:
				return json.dumps({})