import settings
import requests, json

class APIRequest():

    def send(url, data):
        resp = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json', 'accept': 'application/json'}, verify=settings.SSL_VERIFY)
        return resp.json()
