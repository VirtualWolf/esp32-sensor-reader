import urequests
import ujson
import config
import logger

c = config.read_configuration()

def send(payload):
    url = c['endpoint']
    headers = {'X-Weather-API': c['api_key']}

    if c['local_only'] is not True:
        try:
            r = urequests.post(url, headers=headers, json=payload)
            logger.log('Posted data, received status code: %s' % r.status_code)
            r.close()
        except Exception as e:
            print (e)
