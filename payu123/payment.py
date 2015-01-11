import base, settings

class PaymentRequest(base.APIRequest):
    
    def get_payment_methods(self):
        data = {}
        data['command'] = 'GET_PAYMENT_METHODS'

        resp = self.send(settings.PAYMENTS_URL, data=data)

        return resp

    def ping(self):

        data = {}
        data['command'] = 'PING'

        resp = self.send(settings.PAYMENTS_URL, data=data)

        return resp['code'] == 'SUCCESS'
