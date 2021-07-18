import os
import gc
import re
import uasyncio as asyncio
import machine
import sensor
import logger
import config

c = config.read_configuration()

async def get_log(writer):
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

    await writer.drain()
    writer.close()
    await writer.wait_closed()

    gc.collect()

async def clear_log(writer):
    with open('log', 'w'):
        pass

    logger.log('Log file cleared', write_to_log=True)
    await send_response(writer, 'Log file cleared!', 'text/plain')

async def reset_board(writer):
    logger.log('Board reset requested', write_to_log=True)
    await send_response(writer, 'Resetting board...', 'text/plain')
    await asyncio.sleep(2)

    machine.reset()

async def send_response(writer, content, content_type, response_code='200 OK'):
    writer.write(b'HTTP/1.1 %s\r\n' % response_code)

    if content_type != '':
        writer.write(b'Content-Type: %s\r\n' % content_type)

    writer.write(b'Connection: close\r\n')
    writer.write(b'\r\n')

    if content != '':
        writer.write(b'%s\r\n' % content)
        writer.write(b'\r\n')

    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def serve(reader, writer):
    req = await reader.readline()

    is_authorised_request = False

    while True:
        h = await reader.readline()

        if 'X-API-Key: %s\r\n' % c['api_key'] in h:
            is_authorised_request = True

        if h in (b'', b'\r\n'):
            break

    if 'POST /reset' in req:
        if is_authorised_request:
            await reset_board(writer)
        else:
            await send_response(writer, '403 Forbidden', 'text/plain', '403 FORBIDDEN')
    elif 'GET /log ' in req:
        await get_log(writer)
    elif 'DELETE /log ' in req:
        if is_authorised_request:
            await clear_log(writer)
        else:
            await send_response(writer, '403 Forbidden', 'text/plain', '403 FORBIDDEN')
    elif 'GET / ' in req:
        await send_response(writer, sensor.get_current_data(), 'application/json')
    else:
        await send_response(writer, 'Resource not found', 'text/plain', '404 NOT FOUND')

    gc.collect()
