from . import settings
import requests, json

def _has_parameter(_dict, param):
    if type(_dict) != dict:
        return False

    values = param.split('.', 1)

    if values[0] not in _dict:
        return False

    if len(values) > 1:
        return _has_parameter(_dict[values[0]], values[1])

    return True


def _validate_request_parameters(_dict, req_groups):

    def get_prefix_key(prefix, key):
        if prefix == '':
            return key

        return prefix +'.'+ key

    def _validate(group, prefix=''):
        for key, requirements in group.iteritems():
            parameter = get_prefix_key(prefix, key)

            if not requirements:
                if not _has_parameter(_dict, parameter):
                    raise ParameterNotFound(parameter)
            else:
                _validate(requirements, parameter)

        return True

    for group in req_groups:
        _validate(group)

def send(url, _dict={}, data=None):

    if not data:

        _dict['language'] = settings.REQUEST_LANGUAGE
        _dict['test'] = settings.IS_TEST_REQUEST
        _dict['merchant'] = {}

        _dict['merchant']['apiLogin'] = settings.API_LOGIN
        _dict['merchant']['apiKey'] = settings.API_KEY

        data = json.dumps(_dict)

    resp = requests.post(url, data=data, headers={'content-type': 'application/json', 'accept': 'application/json'}, verify=settings.SSL_VERIFY)
    resp = resp.json()

    if resp['code'] == 'ERROR':
        raise RequestError(resp['error'])

    return resp


class RequestError(Exception):

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error

class ParameterNotFound(RequestError):    
    pass
