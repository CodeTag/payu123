from . import base, settings

class ReportRequest(base.APIRequest):

    @staticmethod
    def ping():
        data = {}
        data['command'] = 'PING'

        resp = ReportRequest.send(settings.REPORTS_URL, data=data)

        return resp['code'] == 'SUCCESS'
