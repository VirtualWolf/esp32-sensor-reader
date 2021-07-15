import uasyncio as asyncio
import sensor
import logger

async def serve(reader, writer):
    req = await reader.readline()
    logger.log(req)

    while True:
        h = await reader.readline()
        if h in (b'', b'\r\n'):
            break

    response = (b'HTTP/1.1 200 OK\n'
                b'Content-Type: application/json\n\n'
                b'%s' % {'hello': 'world'})

    writer.write(response)
    await writer.drain()

    writer.close()
    await writer.wait_closed()
