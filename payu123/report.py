from . import base, settings

def ping():
    data = {}
    data['command'] = 'PING'

    resp = base.send(settings.REPORTS_URL, data=data)

    return resp['code'] == 'SUCCESS'
