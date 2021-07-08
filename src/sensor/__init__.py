import gc
import utime
from machine import Pin
import dht
import ujson

class Sensor():
    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.timestamp = 0
        self.name = 'outdoor'

    def read_sensor(self):
        while True:
            print('Reading sensor...')
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
                    self.timestamp = utime.time() + 946684800

                    print('First reading, values are %s˚ & %s' % (self.temperature, self.humidity))
                else:
                    if abs(temperature - self.temperature) > 0.3:
                        print('Skipping because difference is too large. Currently %s, got %s' % (self.temperature, temperature))
                    else:
                        self.temperature = sensor.temperature()
                        self.humidity = sensor.humidity()
                        self.timestamp = utime.time() + 946684800

                        print('Sensor read at %s, new values: %s & %s' % (self.timestamp, self.temperature, self.humidity))

                utime.sleep(30)
            except OSError:
                print('Failed to read sensor')
                utime.sleep(30)

    def get_current_data(self):
        sensor = dht.DHT22(Pin(26))
        sensor.measure()

        jsonData = {
            "name": self.name,
            "timestamp": self.timestamp,
            "temperature": self.temperature,
            "humidity": self.humidity
        }

        return ujson.dumps(jsonData)
