import cherrypy
import json
import time
from get_weather import get_weather

class WeatherService:
    """REST Weather Service"""
    exposed=True

    def GET(self, *uti, **params):
        arduino_ip=cherrypy.request.remote.ip
        weather=None
        with open('weatherconversion.json') as jf:
            weather=get_weather(json.load(jf), arduino_ip)
        return str(weather)



def main():
    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on':True,
            'tools.sessions.storage_type':'file',
            'tools.sessions.storage_path':'./',
            'tools.sessions.timeout':1440
        }
    }
    cherrypy.tree.mount(WeatherService(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
