import requests
import json
import time

n = 2
loops = 3
address = 'http://127.0.0.1:8080/devices'
if __name__ == '__main__':

	for i in range(loops):
		device_id = input('device_id to register: ')
		resources = []
		endpoints = []
		for j in range(2):
			res = input('resource #' + str(j+1) + ' to insert: ')
			resources.append(res)
			endpoint = input('endpoint of res #' + str(j+1) + ': ')
			endpoints.append(endpoint)
		json_data = {}
		json_data['device_id'] = device_id
		json_data['endpoints'] = endpoints
		json_data['resources'] = resources
		json_data_check = {}
		json_data_check['device_id'] = device_id
		for k in range(loops):
			requests.put(address, json = json_data)
			response = requests.post(address, json = json_data_check)
			print(response.json())
			time.sleep(5)
			print("\n")
	print("\n\n Closing...")

