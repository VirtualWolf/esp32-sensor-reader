from ntptime import settime
from utime import sleep
import logger

def update():
    while True:
        logger.log('Updating time from NTP server')
        settime()

        # Sleep for 24 hours
        sleep(86400)
