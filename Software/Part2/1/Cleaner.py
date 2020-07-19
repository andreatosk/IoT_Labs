from threading import Thread
import json
import DeviceManager, ServiceManager
import time

wait_time = 60 # Seconds
delete_margin = 120 # Seconds

class Cleaner():

	def __init__(self):
		cleaner_thread = Thread(target=self.start_cleaning, args=self)

	def start_cleaning(self):
		while True:
			time.sleep(wait_time)

			# Devices
			DeviceManager.get_mem_access()
			json = DeviceManager.get_mem_json()
			for device in json:
				device_time = float(device['insertion_timestamp'])
				actual_time = time.time()
				if actual_time - device_time > delete_margin:
					json.pop(device['device_id'])
			set_mem_json(json)
			DeviceManager.get_file_access()
			filename = DeviceManager.get_filename()
			DeviceManager.unlock_memory()
			with open(filename, 'w') as file:
				json.dumps(json, file)
				file.close()
			DeviceManager.unlock_file()

			#Services
			ServiceManager.get_mem_access()
			json = ServiceManager.get_mem_json()
			for service in json:
				service_time = float(service['insertion_timestamp'])
				actual_time = time.time()
				if actual_time - service_time > delete_margin:
					json.pop(service['service_id'])
			set_mem_json(json)
			ServiceManager.get_file_access()
			filename = ServiceManager.get_filename()
			ServiceManager.unlock_memory()
			with open(filename, 'w') as file:
				json.dumps(json, file)
				file.close()
			ServiceManager.unlock_file()


