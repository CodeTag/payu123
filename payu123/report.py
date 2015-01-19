from . import base, settings

class BaseReport(base.BaseModel):

    @staticmethod
    def ping():
        data = {}
        data['command'] = 'PING'

        resp = base._send(settings.REPORTS_URL, data)

        return resp['code'] == 'SUCCESS'
