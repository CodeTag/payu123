from . import settings
import requests, json, re, types

VALIDATORS = {
    'int': {'validator': lambda v: re.match(r'^\d+$', str(v)) != None},
    'string': {'validator': lambda v: re.match(r'^\w+$', str(v)) != None}
}

class BaseField(object):
    def __init__(self, validator='string', require=False):
        self.validator = VALIDATORS[validator]['validator']
        self.require = require

    def _create(self):
        return None

    def _validate(self, value, name):

        if self.require and value == None:
            raise ValueError('%s is require' % name)
                    
        if value != None and self.validator(value) == False:
            raise ValueError('%s is not valid value for %s' % (value, name))

        return True


class BaseModel(object):

    def __new__(cls, *args, **kwargs):
        if cls is BaseModel:
            raise NotImplementedError('Base Model can not be instantiate')

        return super(BaseModel, cls).__new__(cls, *args, **kwargs)

    def __init__(self, require=False):
        self.require = require

        for key, attr in self._get_attrs():  
            if isinstance(attr, types.ClassType):
                attr = attr()

            attr.require = require or attr.require
            self.__dict__[key] = attr._create()

    def _get_attrs(self):
        keys = filter(self._is_attr, dir(self.__class__))
        fields = vars(self.__class__)

        attrs = {}

        for key in keys:
            attrs[key] = fields[key]

        return attrs.iteritems()

    def _is_attr(self, key):
        attr = getattr(self.__class__, key)

        if isinstance(attr, types.ClassType):
            return issubclass(attr, BaseField) or issubclass(attr, BaseModel)
        
        return isinstance(attr, BaseField) or isinstance(attr, BaseModel)

    def _create(self):
        return self

    def _validate(self, obj=None, parent=None):
        obj = obj or self

        for key, attr in self._get_attrs():
            value = self.__dict__[key] if key in self.__dict__ else None
            name = '%s.%s' % (parent or self.__class__, key)

            if isinstance(attr, types.ClassType):
                attr = attr()

            attr._validate(value, name)

        return True

    def _dict(self):
        _dict = self.__dict__

        for key, value in _dict.iteritems():
            if isinstance(value, BaseModel):
                _dict[key] = value._dict()

        return _dict

def _send(url, _dict={}, data=None):

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
