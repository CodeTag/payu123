from . import base, settings

def get_payment_methods():
    data = {}
    data['command'] = 'GET_PAYMENT_METHODS'

    resp = base.send(settings.PAYMENTS_URL, data=data)

    return resp

def ping():

    data = {}
    data['command'] = 'PING'

    resp = base.send(settings.PAYMENTS_URL, data=data)

    return resp['code'] == 'SUCCESS'
