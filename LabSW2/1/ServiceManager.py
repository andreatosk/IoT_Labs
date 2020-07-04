import cherrypy
import json
import time

registered_services = {}
registered_services_filename = 'services.json'

class ServiceManager(object):
	exposed = True

	def __init___(self):
		global registered_services, registered_services_filename
		registered_services = json.load(registered_services_filename)
		self.exposed = True


	def bad_request(recieved_json):
		if len(recieved_json) != 4:
			return True, 'Incorrect number of arguments'
		for argument in recieved_json:
			if len(argument) < 1:
				return True, 'Invalid arguments'
		if not isinstance(recieved_json['endpoints'], list):
			return True, '"endpoints" field has to be an array/list'
		for endpoint in recieved_json['endpoints']:
			if len(endpoint) < 1:
				return True, "Invalid endpoint(s)"
		if not isinstance(recieved_json['insertion_timestamp'], str):
			return True, '"insertion_timestamp" has to be a string'
		global registered_services
		if recieved_json['service_id'] in registered_services.keys():
			return True, 'service_id already exists'
		return False, ''


	@cherrypy.expose
	@cherrypy.tools.json_in()
	def PUT(self):
		global registered_services
		recieved_json = cherrypy.request.json

		error, response = ServiceManager.bad_request(recieved_json)
		if error is True:
			cherrypy.response.status = 400
			return response

		new_service = {}
		new_service['service_id'] = recieved_json['service_id']
		new_service['description'] = recieved_json['description']
		new_service['endpoints'] = []
		for endpoint in recieved_json['endpoints']:
			new_service['endpoints'].append(endpoint)
		new_service['insertion_timestamp'] = str(time.time())
		registered_services[new_service['service-id']] = new_service
		
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
