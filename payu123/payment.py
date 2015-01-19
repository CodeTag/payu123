from . import base, settings

class BasePayment(base.BaseModel):

    @staticmethod
    def get_payment_methods():
        data = {}
        data['command'] = 'GET_PAYMENT_METHODS'

        resp = base._send(settings.PAYMENTS_URL, data)

        return resp

    @staticmethod
    def ping():

        data = {}
        data['command'] = 'PING'

        resp = base._send(settings.PAYMENTS_URL, data)

        return resp['code'] == 'SUCCESS'
