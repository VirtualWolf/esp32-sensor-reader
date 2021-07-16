import os
import gc
import uasyncio as asyncio
import sensor
import logger

async def serve(reader, writer):
    req = await reader.readline()

    while True:
        h = await reader.readline()
        if h in (b'', b'\r\n'):
            break

    if 'GET /log ' in req:
        # Full credit to https://github.com/marcidy/micropython-uasyncio-webexample for this!
        file_stat = os.stat('log')
        file_size = file_stat[6]

        writer.write(b'HTTP/1.1 200 OK\r\n')
        writer.write(b'Content-Type: text/plain\r\n')
        writer.write(b'Content-Length: %s\r\n' % file_size)
        writer.write(b'Accept-Ranges: none\r\n')
        writer.write(b'Transfer-Encoding: chunked\r\n')
        writer.write(b'Connection: close\r\n')
        writer.write(b'\r\n')

        await writer.drain()
        gc.collect()

        max_chunk_size = 1024

        with open('log') as file:
            for x in range(0, file_size, max_chunk_size):
                chunk_size = min(max_chunk_size, file_size - x)
                chunk_header = "{:x}\r\n".format(chunk_size).encode('utf-8')
                writer.write(chunk_header)
                writer.write(file.read(chunk_size))
                writer.write(b'\r\n')
                await writer.drain()
                gc.collect()

        writer.write(b"0\r\n")
        writer.write(b"\r\n")
    else:
        current_data = sensor.get_current_data()

        writer.write(b'HTTP/1.1 200 OK\r\n')
        writer.write(b'Connection: close\r\n')
        writer.write(b'Content-Type: application/json\r\n')
        writer.write(b'\r\n')
        writer.write(b'%s\r\n' % current_data)
        writer.write(b'\r\n')


    await writer.drain()
    writer.close()
    await writer.wait_closed()

    gc.collect()
