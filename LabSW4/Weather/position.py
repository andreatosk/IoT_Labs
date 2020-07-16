import json
import requests

APIserver = 'http://ip-api.com/'


def get_position(ipaddress=''):
    #se non viene passato un indirizzo ip, di default
    #il server risponde con le info sull'indirizzo da cui
    #viene interrogato
    global APIserver
    url=APIserver+'json/'+ipaddress+'?fields=status,lon,lat'
    #mi interessano status = [ 'success' | 'fail' ]
    #               lon, lat : float

    try:
        r=requests.get(url)
    except requests.exceptions.RequestException as e:
        return False

    
    data=json.loads(r.content)
    if data["status"] != 'success':
        #errore del server 'ip-api'
        #posso gestirlo come un errore di connessione
        return False


    #success
    del data['status']

    return data

def main():
    print(get_position())

if __name__=='__main__':
    main()
