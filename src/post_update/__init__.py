import urequests
import ujson
import config
import logger
import post_update.queue as queue

c = config.read_configuration()

def send(payload):
    url = c['endpoint']
    headers = {'X-Weather-API': c['api_key']}

    if c['local_only'] is not True:
        r = urequests.post(url, headers=headers, json=payload)
        logger.log('Posted data, received status code: %s' % r.status_code)

        if r.status_code != 204:
            raise Exception('Status was not 204, got %d' % r.status_code)

        r.close()
