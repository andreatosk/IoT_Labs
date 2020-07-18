import requests
import json
import time
from position import get_position


weather_server='http://www.7timer.info/bin/civil.php'

def convert_data(row_data, jdict):
    clean_data={}
    base_time=int(row_data["init"][8:])
    for data in row_data['dataseries']:
        key=str((base_time+int(data['timepoint']))%24)
        clean_data[key]={}
        #temperature
        clean_data[key]['temperature']=str(data['temp2m'])+' deg Cel'
        #wind
        clean_data[key]['wind']=jdict['wind10m']['values'][str(data['wind10m']['speed'])]+jdict['wind10m']['unit']+', '+data['wind10m']['direction']
        #weather
        if data['prec_type'] not in jdict['prec_type'].keys():
            cc=int(data['cloudcover'])
            wstr=jdict['hour'][key]
            if cc < 5:
                clean_data[key]['weather']='clear '+wstr
            #elif cc >3 and cc <=7:
            #    clean_data[key]['weather']='part. cloudy '+wstr
            else:
                clean_data[key]['weather']='cloudy '+wstr
        else:
            clean_data[key]['weather']=jdict['prec_type'][data['prec_type']]+' '+jdict['prec_amount']['values'][str(data['prec_amount'])]+jdict['prec_amount']['unit']
        #humidity
        clean_data[key]['humidity']='humidity '+data['rh2m']

    return clean_data



def get_weather(jdict, ipaddress=''):
    global weather_server
    
    #SOLO PER IL DEBUG
    params=get_position(ipaddress)
    while(type(params)==type(True) and not params):
        #qualcosa è andato storto, riprovo tra due secondi
        time.sleep(2)
        params=get_position(ipaddress)



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

    response=json.loads(r.content)
    #mi servono solo i primi 7 campi della lista "dataseries": salvo solo il meteo delle prossime 24h
    del response['dataseries'][8:]
    return convert_data(response, jdict)


def main():
    today_forecast=None
    with open('weatherconversion.json') as jf:
        today_forecast=get_weather(json.load(jf))
    print(today_forecast)


if __name__ == '__main__':
    main()