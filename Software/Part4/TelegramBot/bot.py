from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import requests
import json

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

import DeviceManager
import ServiceManager
import UserManager

bot_token = '1234270596:AAECZOBEe3E3b-r0QQz2j3LprxHJga6qikA' # Per le API Telegram
catalog_address = 'http://127.0.0.1:8080/'

devices_filename = DeviceManager.DeviceManager.get_filename()
users_filename = UserManager.UserManager.get_filename()
services_filename = ServiceManager.ServiceManager.get_filename()

def get_chat_id(update): 
	return update.effective_chat.id # Restituisce la chat ID per l'invio dei messaggi

# Formatta le informazioni del dispositivo
def format_device(device_json):
	string = ''
	string += 'Device ID: ' + device_json['device_id']
	string += 'Resources: '
	for resource in device_json['resources']:
		string += '\n\t\t' + resource
	string += 'Endpoints: '
	for endpoint in device_json['endpoints']:
		string += '\n\t\t' + endpoint
	string += '\nTimestamp: ' + device_json['insertion_timestamp']
	string += '\n\n'
	return string

def devices(update, context):
	arguments = context.args
	chat_id = get_chat_id(update)
	bot = context.bot
	endpoint = catalog_address + 'devices'
	request_json = {}

	if len(arguments) == 0: # Non è fornito un ID al comando
		request_json['device_id'] = ''
		response = requests.post(endpoint, json=request_json)
		response_json = response.json()
		if response.status_code != 200:
			msg = 'Something went wrong processing your request.'
			bot.send_message(chat_id=chat_id, text=msg)
			return

		msg = 'Devices IDs:\n'
		for device_id in response_json:
			msg += device_id + '\n'	# "Incolla" tutti gli ID
		bot.send_message(chat_id=chat_id, text=msg)
	else: # È fornito almeno un ID
		msg = 'Data:\n'
		for device_id in arguments:
			request_json['device_id'] = device_id
			response = requests.post(endpoint, json=request_json)
			try:
				response_json = response.json()
				if response.status_code != 200:
					msg = 'Something went wrong processing your request.'
					bot.send_message(chat_id=chat_id, text=msg)
					return
				msg += format_device(response_json)
			except:	# L'eccezione è scatenata se e solo se l'ID non è presente in memoria
				msg += device_id + " not found.\n"
		bot.send_message(chat_id=chat_id, text=msg)

# Formatta le informazioni utente
def format_user(user_json):
	string = ''
	string += 'User ID: ' + user_json['user_id']
	string += '\nName: ' + user_json['name']
	string += '\nSurname: ' + user_json['surname']
	string += '\nEmails:'
	for email in user_json['email']:
		string += '\n\t\t' + email
	string += '\n\n'
	return string
# Vedere commenti di devices(), struttura simile
def users(update, context):
	arguments = context.args
	chat_id = get_chat_id(update)
	bot = context.bot
	endpoint = catalog_address + 'users'
	request_json = {}

	if len(arguments) == 0:
		request_json['user_id'] = ''
		response = requests.post(endpoint, json=request_json)
		response_json = response.json()
		if response.status_code != 200:
			msg = 'Something went wrong processing your request.'
			bot.send_message(chat_id=chat_id, text=msg)
			return

		msg = 'Users IDs:\n'
		for user_id in response_json.keys():
			msg += user_id + '\n'
		bot.send_message(chat_id=chat_id, text=msg)
	else:
		msg = 'Data:\n'
		for user_id in arguments:
			request_json['user_id'] = user_id
			response = requests.post(endpoint, json=request_json)
			try:
				response_json = response.json()
				print(response_json)
				if response.status_code != 200:
					msg = 'Something went wrong processing your request.'
					bot.send_message(chat_id=chat_id, text=msg)
					return
				msg += format_user(response_json)
			except:
				msg += user_id + " not found.\n"
		bot.send_message(chat_id=chat_id, text=msg)

# Formatta le informazioni del servizio
def format_service(service_json):
	string = ''
	string += 'Service ID: ' + service_json['service_id']
	string += '\nDescription: ' + service_json['description']
	string += '\nEndpoints: '
	for endpoint in service_json['endpoints']:
		string += '\n\t\t' + endpoint
	print(service_json['endpoints'])
	string += '\nTimestamp: ' + service_json['insertion_timestamp']
	print(service_json['insertion_timestamp'])
	string += '\n\n'
	return string

# Vedere commenti di devices(), struttura simile
def services(update, context):
	arguments = context.args
	chat_id = get_chat_id(update)
	bot = context.bot
	endpoint = catalog_address + 'services'
	request_json = {}

	if len(arguments) == 0:
		request_json['service_id'] = ''
		response = requests.post(endpoint, json=request_json)
		response_json = response.json()
		if response.status_code != 200:
			msg = 'Something went wrong processing your request.'
			bot.send_message(chat_id=chat_id, text=msg)
			return

		msg = 'Services IDs:\n'
		for service_id in response_json:
			msg += service_id + '\n'
		bot.send_message(chat_id=chat_id, text=msg)
	else:
		msg = 'Data:\n'
		for service_id in arguments:
			request_json['service_id'] = service_id
			response = requests.post(endpoint, json=request_json)
			try:
				response_json = response.json()
				if response.status_code != 200:
					msg = 'Something went wrong processing your request.'
					bot.send_message(chat_id=chat_id, text=msg)
					return
				msg += format_service(response_json)
			except:
				msg += service_id + " not found.\n"
		bot.send_message(chat_id=chat_id, text=msg)


def help(update, context):
	chat_id = get_chat_id(update)
	bot = context.bot

	msg = '/help' + '\n'
	msg += 'Display this message.'
	bot.send_message(chat_id=chat_id, text=msg)

	msg = '/services' + '\n'
	msg += 'Gets all services\' ids if sent alone, or retrieves informations about all the white-space seprated service ids sent along\n\n'
	msg += 'e.g. "/services", "/services http_418 tncrd_cld"'
	bot.send_message(chat_id=chat_id, text=msg)

	msg = '/devices' + '\n'
	msg += 'Gets all devices\' ids if sent alone, or retrieves informations about all the white-space seprated device ids sent along\n\n'
	msg += 'e.g. "/devices", "/devices http_418 tncrd_cld"'
	bot.send_message(chat_id=chat_id, text=msg)

	msg = '/users' + '\n'
	msg += 'Gets all users\' ids if sent alone, or retrieves informations about all the white-space seprated user ids sent along\n\n'
	msg += 'e.g. "/users", "/users http_418 tncrd_cld"'
	bot.send_message(chat_id=chat_id, text=msg)



if __name__ == '__main__':
	updater = Updater(bot_token, use_context=True)
	dispatcher = updater.dispatcher

	# Declaring Handlers
	devices_handler = CommandHandler('devices', devices)
	users_handler = CommandHandler('users', users)
	services_handler = CommandHandler('services', services)
	help_handler = CommandHandler('help', help)

	# Dispatching Handlers
	dispatcher.add_handler(devices_handler)
	dispatcher.add_handler(users_handler)
	dispatcher.add_handler(services_handler)
	dispatcher.add_handler(help_handler)

	# Starting Execution

	updater.start_polling()
	updater.idle()


