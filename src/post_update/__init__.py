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
        try:
            r = urequests.post(url, headers=headers, json=payload)
            logger.log('Posted data, received status code: %s' % r.status_code)

            if r.status_code != 204:
                raise Exception('Status was not 204')

            r.close()
        except Exception as e:
            logger.log('Failed to post update, writing to queue as %s.json: %s' % (str(payload['timestamp']), e), write_to_log=True)

            queue.write_to_queue(payload)
