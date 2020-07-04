import requests as r
import json


address = 'http://127.0.0.1:8080/'



if __name__ == '__main__':
	print("Test Software for Excercise [1]")

	#1
	print("Retrieving broker info")
	request = r.get(address + 'broker_info')
	print(request.json())

	#2
	print("\nRetrieving all registered services")
	request_json = {}
	request_json['service_id'] = ''
	request = r.post(address + 'services', json=request_json)
	print(request.json())

	#3
	service_id = input("\nEnter a ServiceID to search for: ")
	request_json['service_id'] = service_id
	request = r.post(address + 'services', json=request_json)
	print(request.json())

	#4
	print("\nRetrieving all users")
	request_json = {}
	request_json['user_id'] = ''
	request = r.post(address + 'users', json=request_json)
	print(request.json())


	#5
	user_id = input("\nEnter a UserID to search for: ")
	request_json['user_id'] = user_id
	request = r.post(address + 'users', json=request_json)
	print(request.json())
