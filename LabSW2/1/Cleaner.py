import threading
import json
import DeviceManager, ServiceManager
import time

minutes = 60
wait_time = 5*minutes
delete_margin = 2*minutes

class Cleaner(threading.Thread):

	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		while True:
			print('Cleaning')
			time.sleep(wait_time)

			# Devices
			DeviceManager.DeviceManager.get_memory_access()
			old_json = DeviceManager.DeviceManager.get_mem_json()
			new_json = {}

			for device in old_json:
				device_time = float(old_json[device]['insertion_timestamp'])
				actual_time = time.time()
				if actual_time - device_time <= delete_margin:
					new_json[device] = old_json[device]


			DeviceManager.DeviceManager.set_mem_json(new_json)
			DeviceManager.DeviceManager.get_file_access()
			filename = DeviceManager.DeviceManager.get_filename()
			DeviceManager.DeviceManager.unlock_memory()
			with open(filename, 'w') as file:
				json.dump(new_json, file)
				file.close()
			DeviceManager.DeviceManager.unlock_file()
			

			#Services
			ServiceManager.ServiceManager.get_memory_access()
			old_json = ServiceManager.ServiceManager.get_mem_json()
			new_json = {}
			for service in old_json:
				service_time = float(old_json[service]['insertion_timestamp'])
				actual_time = time.time()
				if actual_time - service_time <= delete_margin:
					new_old_json[device] = old_json[device]
			ServiceManager.ServiceManager.set_mem_json(new_json)
			ServiceManager.ServiceManager.get_file_access()
			filename = ServiceManager.ServiceManager.get_filename()
			ServiceManager.ServiceManager.unlock_memory()
			with open(filename, 'w') as file:
				json.dump(new_json, file)
				file.close()
			ServiceManager.ServiceManager.unlock_file()


