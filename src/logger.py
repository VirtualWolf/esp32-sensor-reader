import utime

def log (message):
    year, month, day, hour, minute, second, weekday, yearday = utime.gmtime()

    now = '{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(year, month, day, hour, minute, second)

    print('[%s] %s' % (now, message))
