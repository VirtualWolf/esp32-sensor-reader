import gc
import utime
from machine import Pin
import dht
import ujson
import uasyncio as asyncio
import post_update
import config
import logger

c = config.read_configuration()

class Sensor():
    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.timestamp = 0
        self.name = c['sensor_name']

    async def read_sensor(self):
        while True:
            logger.log('Reading sensor...')

            try:
                sensor = dht.DHT22(Pin(26))
                sensor.measure()

                temperature = sensor.temperature()
                humidity = sensor.humidity()

                if self.temperature == 0 and self.humidity == 0:
                    self.temperature = temperature
                    self.humidity = humidity
                    # Embedded systems epoch is 2000-01-01 00:00:00 UTC, so we need
                    # to add 946684800 seconds onto it to turn it into a UNIX epoch
                    # timestamp
                    self.timestamp = (utime.time() + 946684800) * 1000

                    logger.log('First reading, values are %s˚ & %s%%' % (self.temperature, self.humidity))
                else:
                    if abs(temperature - self.temperature) > 0.3:
                        logger.log('Skipping because difference is too large. Currently %s, got %s' % (self.temperature, temperature))
                    else:
                        self.temperature = sensor.temperature()
                        self.humidity = sensor.humidity()
                        self.timestamp = (utime.time() + 946684800) * 1000

                        logger.log('Sensor read at %s, new values: %s & %s%%' % (self.timestamp, self.temperature, self.humidity))

                gc.collect()
                # logger.log('Free memory: %s, allocated memory: %s' % (gc.mem_free(), gc.mem_alloc()))

            except Exception as e:
                logger.log('Failed to read sensor: '  + str(e), write_to_log=True)

            await asyncio.sleep(30)

    async def send_current_data(self):
        while True:
            payload = {
                'sensor_name': self.name,
                'timestamp': self.timestamp,
                'temperature': self.temperature,
                'humidity': self.humidity
            }

            if payload['timestamp'] != 0:
                try:
                    post_update.send(payload)
                except Exception as e:
                    logger.log('Failed to post update, writing to queue as %s.json: %s' % (str(payload['timestamp']), e), write_to_log=True)
                    post_update.queue.write_to_queue(payload)

            await asyncio.sleep(30)


    def get_current_data(self):
        current_data = ujson.dumps({
            "name": self.name,
            "timestamp": self.timestamp,
            "temperature": self.temperature,
            "humidity": self.humidity
        })

        return current_data
