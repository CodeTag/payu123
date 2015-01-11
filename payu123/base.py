import settings
import requests, json

class APIRequest():

    def send(self, url, data):

        data['language'] = settings.REQUEST_LANGUAGE
        data['test'] = settings.IS_TEST_REQUEST
        data['merchant'] = {}

        data['merchant']['apiLogin'] = settings.API_LOGIN
        data['merchant']['apiKey'] = settings.API_KEY

        resp = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json', 'accept': 'application/json'}, verify=settings.SSL_VERIFY)
        resp = resp.json()

        if resp['code'] == 'ERROR':
            raise RequestError(resp['error'])

        return resp


class RequestError():

    def __init__(self, error):
        self.error

    def __str__(self):
        return self.error

