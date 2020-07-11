import cherrypy
import json
import time
from get_weather import get_weather

class WeatherService:
    """REST Weather Service"""

    def __new_weather(self, key):
        arduino_ip=cherrypy.request.remote.ip

        weather=None
        with open('weatherconversion.json') as jf:
            weather=get_weather(json.load(jf), arduino_ip)
            cherrypy.session['weather']=weather
            curr_w=weather[key]
        return curr_w

    def __retrieve_weather(self, key):
        return cherrypy.session['weather'][key]



    exposed=True

    def GET(self, *uri, **params):
        exp=''
        if len(uri) > 1 or len(params) != 0:
            #error
            pass

        if len(uri) == 1 and uri[0] == 'new':
            cherrypy.lib.sessions.expire()
            #exp='Session expired.<br>'

        hour=time.localtime().tm_hour
        key=str(((hour+3)//3)*3)
        if 'weather' in cherrypy.session.keys():
            curr_w=self.__retrieve_weather(key)
        else:
            curr_w=self.__new_weather(key)
        return exp+json.dumps(curr_w)



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
