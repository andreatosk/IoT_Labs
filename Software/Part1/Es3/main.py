import cherrypy
import json

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

class  unitConverter(object):
	exposed = True

	@cherrypy.expose
	@cherrypy.tools.json_in() # Stando a StackOverflow, senza questa non funziona
	def PUT(*uri, **params):
		request_json = cherrypy.request.json
		source_unit = request_json['originalUnit']
		target_unit = request_json['targetUnit']
		values = request_json['values']

		response_json = {}
		response_json['originalUnit'] = source_unit
		response_json['targetUnit'] = target_unit
		response_json['originalValues'] = values
		if source_unit == target_unit:
			response_json['originalValues'] = values
			response_json['convertedValues'] = values
			return json.dumps(response_json)

		response_values = []

		if source_unit == 'C':
			if target_unit == 'F':
				for value in values:
					response_values.append(celsiusToFar(value))
			else:
				for value in values:
					response_values.append(celsiusToKelvin(value))


		elif source_unit == 'K':
			if target_unit == 'C':
				for value in values:
					response_values.append(kelvinToCelsius(value))
			else:
				for value in values:
					response_values.append(kelvinToFar(value))


		elif source_unit == 'F':
			if target_unit == 'C':
				for value in values:
					response_values.append(farToCelsius(value))
			else:
				for value in values:
					response_values.append(farToKelvin(value))


		else:
			cherrypy.response.status = 418
			return "q.q"

		response_json['convertedValues'] = response_values
		return json.dumps(response_json)


if __name__ == "__main__":
    conf = {
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on':True
        }
    }
    cherrypy.quickstart(unitConverter,'/converter', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()