import cherrypy
import json
import time

registered_users = {}
registered_users_filename = 'users.json'

class UserManager(object):
	exposed=True
	
	def __init__(self):
		global registered_users, registered_users_filename
		try:
			with open(registered_users_filename, 'r') as file:
				registered_users = json.load(file)
		except:
			pass # JSON vuoti

	# Questa funzione implementa alcuni controlli basilari sul JSON ricevuto
	def bad_request(recieved_json):
		if len(recieved_json) != 4:
			return True, 'Incorrect number of arguments'

		for argument in recieved_json:
			if len(argument) < 1:
				return True, 'Invalid arguments'

		try:
			if not isinstance(recieved_json['email'], list):
				return True, '"email" field has to be an array/list'
			for email in recieved_json['email']:
				if len(email) < 1:
					return True, 'Invalid email(s)'
		except:
			return True, 'Missing "email" field'


		global registered_users
		try:
			if recieved_json['user_id'] in registered_users.keys():
				return True, "user_id already exists"
			return False, ''
		except:
			return True, 'Missing "user_id" field'

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def PUT(self):
		global registered_users
		recieved_json = cherrypy.request.json

		error, response = UserManager.bad_request(recieved_json)
		if error is True:
			cherrypy.response.status = 400
			return response

		registered_users[recieved_json['user_id']] = recieved_json  
		with open(registered_users_filename, 'w') as file:
			json.dump(registered_users, file)
		# Sarebbe carino trovare il modo di poter operare in 'append' senza dover riscrivere l'intero file

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def POST(self):
		# Se 'user_id' è vuoto, ritorna tutto
		# Se 'user_id' contiene un id, ritorna quello
		global registered_users
		recievied_json = cherrypy.request.json

		try:
			request = recievied_json['user_id']
		except:
			return 'Missing "user_id" field.'


		if request == '':
			return json.dumps(registered_users)
		else:
			return json.dumps(registered_users[request])
