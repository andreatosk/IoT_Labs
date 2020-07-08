from telegram.ext import Updater, CommandHandler
import requests
import json


import DeviceManager
import ServiceManager
import UserManager

bot_token = '1234270596:AAECZOBEe3E3b-r0QQz2j3LprxHJga6qikA'
catalog_address = 'http://127.0.0.1:8080/'

devices_filename = DeviceManager.DeviceManager.get_filename()
users_filename = UserManager.UserManager.get_filename()
services_filename = ServiceManager.ServiceManager.get_filename()

def chat_id(update):
	return update.effective_chat.id

def devices(update, context):
	arguments = context.args
	chat_id = chat_id(update)
	bot = context.bot
	endpoint = catalog_address + 'devices'
	request_json = {}

	if len(arguments) == 0:
		request_json['device_id'] = ''
		response = requests.post(endpoint, json=request_json)
		response_json = response.json()
		if response.status_code != 200:
			msg = 'Something went wrong processing your request.'
			bot.send_message(chat_id=chat_id, msg=msg)
			return

		msg = 'Devices IDs:\n'
		for device_id in response_json.keys():
			msg += device_id + '\n'
		bot.send_message(chat_id=chat_id, msg=msg)
	else:
		msg = 'Data:\n'
		for device_id in arguments:
			request_json['device_id'] = device_id
			response = requests.post(endpoint, json=request_json)
			try:
				response_json = response.json()
				if response.status_code != 200:
					msg = 'Something went wrong processing your request.'
					bot.send_message(chat_id=chat_id, msg=msg)
					return
				msg += str(response_json)
			except:
				msg += device_id + " not found.\n"
		bot.send_message(chat_id=chat_id, msg=msg)

def users(update, context):
	arguments = context.args
	chat_id = chat_id(update)
	bot = context.bot
	endpoint = catalog_address + 'users'
	request_json = {}

	if len(arguments) == 0:
		request_json['user_id'] = ''
		response = requests.post(endpoint, json=request_json)
		response_json = response.json()
		if response.status_code != 200:
			msg = 'Something went wrong processing your request.'
			bot.send_message(chat_id=chat_id, msg=msg)
			return

		msg = 'Users IDs:\n'
		for user_id in response_json.keys():
			msg += user_id + '\n'
		bot.send_message(chat_id=chat_id, msg=msg)
	else:
		msg = 'Data:\n'
		for user_id in arguments:
			request_json['user_id'] = user_id
			response = requests.post(endpoint, json=request_json)
			try:
				response_json = response.json()
				if response.status_code != 200:
					msg = 'Something went wrong processing your request.'
					bot.send_message(chat_id=chat_id, msg=msg)
					return
				msg += str(response_json)
			except:
				msg += user_id + " not found.\n"
		bot.send_message(chat_id=chat_id, msg=msg)


def services(update, context):
	arguments = context.args
	chat_id = chat_id(update)
	bot = context.bot
	endpoint = catalog_address + 'services'
	request_json = {}

	if len(arguments) == 0:
		request_json['service_id'] = ''
		response = requests.post(endpoint, json=request_json)
		response_json = response.json()
		if response.status_code != 200:
			msg = 'Something went wrong processing your request.'
			bot.send_message(chat_id=chat_id, msg=msg)
			return

		msg = 'Services IDs:\n'
		for service_id in response_json.keys():
			msg += service_id + '\n'
		bot.send_message(chat_id=chat_id, msg=msg)
	else:
		msg = 'Data:\n'
		for service_id in arguments:
			request_json['service_id'] = service_id
			response = requests.post(endpoint, json=request_json)
			try:
				response_json = response.json()
				if response.status_code != 200:
					msg = 'Something went wrong processing your request.'
					bot.send_message(chat_id=chat_id, msg=msg)
					return
				msg += str(response_json)
			except:
				msg += service_id + " not found.\n"
		bot.send_message(chat_id=chat_id, msg=msg)


def help(update, context):
	chat_id = chat_id(update)
	bot = context.bot

	msg = '/help' + '\n'
	msg += 'Display this message.'
	bot.send_message(chat_id=chat_id, text=msg)

	msg = '/services' + '\n'
	msg += 'Gets all services\' ids if sent alone, or retrieves informations about all the white-space seprated service ids sent along\n\n'
	msg += 'e.g. "/services", "/services hjk_418 tncrd_cld"'
	bot.send_message(chat_id=chat_id, text=msg)

	msg = '/devices' + '\n'
	msg += 'Gets all devices\' ids if sent alone, or retrieves informations about all the white-space seprated device ids sent along\n\n'
	msg += 'e.g. "/devices", "/devices hjk_418 tncrd_cld"'
	bot.send_message(chat_id=chat_id, text=msg)

	msg = '/users' + '\n'
	msg += 'Gets all users\' ids if sent alone, or retrieves informations about all the white-space seprated user ids sent along\n\n'
	msg += 'e.g. "/users", "/users hjk_418 tncrd_cld"'
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

	print('Everything went fine. Bot Online.')
	updater.start_polling()
	updater.idle()

