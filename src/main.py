import uasyncio as asyncio
import webserver
import sensor
import logger
import post_update
import set_time

try:
    loop = asyncio.get_event_loop()

    loop.create_task(set_time.update())

    loop.create_task(sensor.read_sensor())
    loop.create_task(sensor.send_current_data())

    loop.create_task(asyncio.start_server(webserver.serve, '0.0.0.0', 80))

    loop.create_task(post_update.queue.process_queue())

    loop.run_forever()
except Exception as e:
    logger.log('Something went very wrong: %s' % e, write_to_log=True)
