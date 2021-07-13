from ntptime import settime
import utime
import logger

def update():
    while True:
        logger.log('Updating time from NTP server')
        settime()

        # Sleep for 24 hours
        utime.sleep(86400)
