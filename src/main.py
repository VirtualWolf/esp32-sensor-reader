import usocket as socket
import _thread
import sensor
import logger

outdoor = sensor.Sensor()
_thread.start_new_thread(outdoor.read_sensor, ())

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(1)

logger.log('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server.accept()

    logger.log('Got a connection from %s!' % client_address[0])

    # Get the client request
    request = client_connection.recv(1024).decode()

    # Send HTTP response
    response = ('HTTP/1.0 200 OK\n'
                'Content-Type: application/json\n\n'
                '%s') % (outdoor.get_current_data())

    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server.close()
