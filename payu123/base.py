import settings
import requests, json

class APIRequest():

    def send(self, url, data):

        data['language'] = settings.REQUEST_LANGUAGE
        data['merchant'] = {}

        data['merchant']['apiLogin'] = settings.API_LOGIN
        data['merchant']['apiKey'] = settings.API_KEY


        resp = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json', 'accept': 'application/json'}, verify=settings.SSL_VERIFY)
        return resp.json()
