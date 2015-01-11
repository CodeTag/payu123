import base, settings

class PaymentRequest(base.APIRequest):
    
    def ping(self):

        data = {}
        data['command'] = 'PING'

        resp = self.send(settings.PAYMENTS_URL, data=data)

        return resp['code'] == 'SUCCESS'
