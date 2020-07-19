import cherrypy
import json
types = {'C','K','F'}



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


    def GET(*uri,**params):
        if(len(uri)>2 and uri[0]!='' and uri[1]!='' and uri[2]!=''):
            src = uri[1]
            tar = uri[2]
            value = uri[0]
            t = ""
            if ((src in types) and (tar in types)):

                if((src=='K')and (tar=='C')):
                    t = str(kelvinToCelsius(int(value)))
                elif((src=='C')and (tar=='K')):
                    t = str(celsiusToKelvin(int(value)))
                elif((src=='C')and (tar=='F')):
                    t = str(celsiusToFar(int(value)))
                elif((src=='F')and (tar=='C')):
                    t = str(farToCelsius(int(value)))
                elif((src=='K')and (tar=='F')):
                    t = str(kelvinToFar(int(value)))
                else:
                    t = str(farToKelvin(int(value)))         
            
            c = {}
            c["originalValue"] = value
            c["sourceUnit"] = src
            c["targetUnit"] = tar
            c["targetValue"] = t
            return json.dumps(c)


if __name__ == "__main__":
    conf = {
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on':True
        }
    }
    cherrypy.quickstart(unitConverter,'/converter',conf)