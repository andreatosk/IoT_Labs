import cherrypy
import json
import time

regiseterd_users = {}
registered_users_filename = 'users.json'

class UserManager(object):

	def __init___(self):
		global registered_users, registered_users_filename
		registered_users = json.load(registered_users_filename)


	def bad_request(recieved_json):
		if len(recieved_json) != 4:
			return True, 'Incorrect number of arguments'
		for argument in recieved_json:
			if len(argument) < 1:
				return True, 'Invalid arguments'
		if not isinstance(recieved_json['email'], list):
			return True, '"email" field has to be an array/list'
		for email in recieved_json['emails']:
			if len(email) < 1:
				return True, 'Invalid email(s)'
		global registered_users
		if recieved_json['user_id'] in registered_users.keys():
			return True, "user_id already exists"
		return False, ''


	@cherrypy.expose
	@cherrypy.tools.json_in()
	def PUT(self):
		global registered_users
		recieved_json = cherrypy.request.json

		error, response = bad_request(recieved_json)
		if error is True:
			cherrypy.response.status = 400
			return response

		new_user = {}
		new_user['user_id'] = recieved_json['user_id']
		new_user['name'] = recieved_json['name']
		new_user['surname'] = recieved_json['surname']
		new_user['email'] = []
		for email in recieved_json['email']:
			with new_user['email'] as emails:
				emails.append(email)
		json.dump(registered_users, registered_users_filename)



	@cherrypy.expose
	@cherrypy.tools.json_in()
	def GET(self):
		# Se 'user_id' è vuoto, ritorna tutto
		# Se 'user_id' contiene un id, ritorna quello
		global registered_users
		recievied_json = cherrypy.request.json
		request = recievied_json['user_id']
		if request == '':
			return json.dumps(registered_users)
		else:
			return json.dumps(registered_users[request])



	@cherrypy.expose
	def POST(self):
		cherrypy.response.status = 403
		return 'Error'



	@cherrypy.expose
	def DELETE(self):
		cherrypy.response.status = 403
		return 'Error'
	

