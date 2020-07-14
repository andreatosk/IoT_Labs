import cherrypy
import json
types = {'C','K','F'}
values = []


def celsiusToKelvin(src):
    return src+273

def kelvinToCelsius(src):
    return src+273  

def celsiusToFar(src):
    return src * (9/5) + 32

def farToCelsius(src):
    return (src-32) * (5/9)

def kelvinToFar(src):
    return (src*9/5) - 459.67

def farToKelvin(src):
    return (src+459.67) * (5/9)

class unitConverter(object):
    exposed = True


    def POST():
        body = cherrypy.request.body.read()
        data = json.loads(body)
        values.append(data)

    def GET():
        t = ""
        for s in values:
            t += s
            t += '\n'
        return t



if __name__ == "__main__":
    conf = {
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on':True
        }
    }
    cherrypy.tree.mount('/log',unitConverter,'/')
    cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
