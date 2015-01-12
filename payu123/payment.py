from . import base, settings

BASE_TRANSACTION_PARAMETERS = {
    'order': {
        'accountId': None, 
        'referenceCode': None, 
        'description': None, 
        'language': None, 
        'signature': None,
    },

    'buyer': {
        'emailAddress': None,
    },

    'additionalValues':{
        'TX_VALUE': {
            'value': None,
            'currency': None,
        }
    },

    'payer':{
        'emailAddress': None,
        'fullName': None,
        'contactPhone': None,
    },

    'paymentMethod': None,

    'extraParameters':{
        'INSTALLMENTS_NUMBER': None,
    },

    'reason': None,
}

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
