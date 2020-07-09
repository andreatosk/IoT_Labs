import requests
import json
from position import get_position
import time

weather_server='http://www.7timer.info/bin/civil.php'

def get_weather():
    global weather_server
    
    #SOLO PER IL DEBUG
    params=get_position()
    while(type(params)==type(True) and not params):
        #qualcosa è andato storto, riprovo
        params=get_position()



    params['unit']='metric'
    params['output']='json'

    try:
        r=requests.get(weather_server, params)
    except requests.exceptions.RequestException as e:
        #da gestire nel chiamante
        return False

    #il json restituito dal server è nella forma:
    #{
    #    "product": "civil",
    #    "init": "2020070900",
    #    "dataseries": [
    #        {
    #        "timepoint": 3, 
            #TIMEPOINT varia di 3 in 3 -> mi serve fino a 24 (perché timepoint parte da 3, quindi le 24 rientrano nel giorno corrente)
    #        "cloudcover": 9,
    #        "lifted_index": -6,
    #        "prec_type": "none",
    #        "prec_amount": 0,
    #        "temp2m": 34,
    #        "rh2m": "57%",
    #        "wind10m": {
    #            "direction": "SW",
    #            "speed": 3
    #        },
    #        "weather": "tsday"
    #        },
    #}

    response=json.loads(r)
    #mi servono solo i primi 7 campi della lista "dataseries"
    del response['dataseries'][8:]
    current_hour=time.localtime().tm_hour



def main():
    #NB tools.session.on
    pass

#mi registro al catalogo dei servizi

if __name__ == '__main__':
    main()