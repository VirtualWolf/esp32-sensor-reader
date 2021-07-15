import uasyncio as asyncio
import sensor
import logger

async def serve(reader, writer):
    req = await reader.readline()

    while True:
        h = await reader.readline()
        if h in (b'', b'\r\n'):
            break

    response = (b'HTTP/1.1 200 OK\n'
                b'Content-Type: application/json\n\n'
                b'%s' % sensor.get_current_data())

    writer.write(response)
    await writer.drain()

    writer.close()
    await writer.wait_closed()
