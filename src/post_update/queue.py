import os
import ujson
import utime
import logger
import post_update

try:
    logger.log('Creating queue directory...')
    os.mkdir('queue')
except Exception as e:
    logger.log('Queue directory already exists, skipping creation')

def write_to_queue(payload):
    try:
        filepath = 'queue/%s.json' % str(payload['timestamp'])
        file = open(filepath, 'w')
        json = ujson.dumps(payload)

        file.write(json)

        file.close()
    except Exception as e:
        logger.log('Failed to write file: ' + e)

def process_queue():
    while True:
        logger.log('Processing queue...')

        files = os.listdir('queue')

        for file in (files):
            logger.log('Reading %s from queue' % file)

            content = open('queue/%s' % file, 'r')
            json = ujson.load(content)
            content.close()

            try:
                post_update.send(json)

                os.remove('queue/%s' % file)
            except Exception as e:
                logger.log(e)

        utime.sleep(300)
