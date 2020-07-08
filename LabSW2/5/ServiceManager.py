import cherrypy
import json
import time

registered_services = {}
registered_services_filename = 'services.json'

class ServiceManager(object):
	exposed = True
	file_locked = False
	memory_locked = False

	def __init__(self):
		global registered_services, registered_services_filename
		try:
			with open(registered_services_filename, 'r') as file:
				registered_services = json.load(file)
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
			if not isinstance(recieved_json['endpoints'], list):
				return True, '"endpoints" field has to be an array/list'
			for endpoint in recieved_json['endpoints']:
				if len(endpoint) < 1:
					return True, "Invalid endpoint(s)"
		except:
			return True, 'Missing "endpoints field'

		try:
			test = recieved_json['service_id']
		except:
			return True, 'Missing "service_id" field'

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

		ServiceManager.get_memory_access()
		if recieved_json['service_id'] not in registered_services.keys():
			new_service = ServiceManager.format_new_service(recieved_json)
			registered_services[recieved_json['service_id']] = new_service
		else:
			registered_services['service_id']['insertion_timestamp'] = str(time.time())
		ServiceManager.memory_unlock()
		ServiceManager.write_to_local()


	@cherrypy.expose
	@cherrypy.tools.json_in()
	def POST(self):
		# Se 'service_id' è vuoto, ritorna tutto
		# Se 'service_id' contiene un id, ritorna quello
		global registered_services
		recievied_json = cherrypy.request.json

		try:
			request = recievied_json['service_id']
		except:
			return 'Missing "service_id" field'

		if request == '':
			return json.dumps(registered_services)
		else:
			try:
				return json.dumps(registered_services[request])
			except:
				return '"service_id" not found'


	def write_to_local():
		global registered_services
		ServiceManager.get_file_access()
		with open(registered_services_filename, 'w') as file:
			json.dump(registered_services, file)
			file.close()
		ServiceManager.file_unlock()

	def get_memory_status():
		return self.memory_locked

	def get_file_status():
		return self.file_locked

	def lock_memory():
		self.memory_locked = True

	def get_memory_access():
		while self.get_memory_status() is True:
			pass
		self.lock_memory()

	def get_file_access():
		while self.get_file_status() is True:
			pass
		self.lock_file()

	def lock_file():
		self.file_locked = True

	def unlock_file():
		self.file_locked = False

	def unlock_memory():
		self.memory_locked = False

	def get_mem_json():
		global registered_services
		return registered_services

	def get_filename():
		global registered_services_filename
		return registered_services_filename

	def set_mem_json(json):
		global registered_services
		registered_services = json