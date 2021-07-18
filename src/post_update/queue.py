import os
import ujson
import uasyncio as asyncio
import _thread
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
        logger.log('Failed to write file: %s' % e, write_to_log=True)

async def process_queue():
    while True:
        logger.log('Processing queue...')

        files = os.listdir('queue')

        for file in files:
            _thread.start_new_thread(send_queue_item, (file, ))

            await asyncio.sleep(2)

        await asyncio.sleep(300)

def send_queue_item(file):
    logger.log('Reading %s from queue' % file)

    content = open('queue/%s' % file, 'r')
    json = ujson.load(content)
    content.close()

    try:
        post_update.send(json)

        logger.log('Successfully posted update: %s' % file, write_to_log=True)

        try:
            os.remove('queue/%s' % file)
        except Exception as e:
            logger.log('Failed to remove file: %s' %  e, write_to_log=True)
    except Exception as e:
        logger.log('Failed to re-post update: %s' % e)
