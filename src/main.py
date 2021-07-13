import usocket as socket
import _thread
import sensor
import logger
import post_update
import set_time

try:
    sensor = sensor.Sensor()

    _thread.start_new_thread(sensor.read_sensor, ())
    _thread.start_new_thread(post_update.queue.process_queue, ())
    _thread.start_new_thread(set_time.update, ())

    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 80

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)

    logger.log('Listening on port %s ...' % SERVER_PORT)

    def handle_request(client):
        logger.log('New thread spawned to handle request')

        r = client.recv(4096)

        if len(r) == 0:
            client.close()
            return

        if 'GET /log ' in str(r):
            with open('log') as f:
                lines = f.readlines()

            logs = (''.join(lines))

            response = ('HTTP/1.0 200 OK\n'
                        'Content-Type: application/json\n\n'
                        '%s') % (logs)
        else:
            response = ('HTTP/1.0 200 OK\n'
                        'Content-Type: application/json\n\n'
                        '%s') % (sensor.get_current_data())

        client.send(response)
        client.close()

    while True:
        (clientsocket, client_address) = server.accept()

        logger.log('Got a connection from %s' % client_address[0])

        _thread.start_new_thread(handle_request, (clientsocket, ))

    server.close()
except Exception as e:
    logger.log('Something went very wrong: %s' % e, write_to_log=True)
