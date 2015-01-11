from . import base, settings

class PaymentRequest(base.APIRequest):
    
    @staticmethod
    def get_payment_methods():
        data = {}
        data['command'] = 'GET_PAYMENT_METHODS'

        resp = PaymentRequest.send(settings.PAYMENTS_URL, data=data)

        return resp

    @staticmethod
    def ping():

        data = {}
        data['command'] = 'PING'

        resp = PaymentRequest.send(settings.PAYMENTS_URL, data=data)

        return resp['code'] == 'SUCCESS'
