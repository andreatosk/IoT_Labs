import cherrypy
import json

import DeviceManager
import UserManager
import ServiceManager
import Cleaner

IP_ADDRESS = "0.0.0.0"
PORT = 8080

class BrokerInfo(object):
	exposed=True

	@cherrypy.expose
	def GET(self):
		global IP_ADDRESS, PORT
		data = {}
		data['ip_address'] = IP_ADDRESS
		data['port'] = PORT
		data['endpoints'] = []
		data['endpoints'].append('/devices')
		data['endpoints'].append('/users')
		data['endpoints'].append('/services')
		data = json.dumps(data)
		return data

if __name__ == "__main__":
	conf = {
		'/' : {
			'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
		}
	}
	
	cherrypy.tree.mount(BrokerInfo(), '/', conf)
	cherrypy.tree.mount(DeviceManager.DeviceManager(), '/devices', conf)
	cherrypy.tree.mount(ServiceManager.ServiceManager(), '/services', conf)
	cherrypy.tree.mount(UserManager.UserManager(), '/users', conf)

	cherrypy.config.update({
		'server.socket_host' : IP_ADDRESS,
		'server.socket_port' : PORT
		})

	Cleaner.Cleaner()
	cherrypy.engine.start()
	cherrypy.engine.block()