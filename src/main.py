# main.py

import usocket as socket
import _thread
import sensor

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print('Listening on port %s ...' % SERVER_PORT)

outdoor = sensor.Sensor()

_thread.start_new_thread(outdoor.read_sensor, ())

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Send HTTP response
    response = ('HTTP/1.0 200 OK\n'
                'Content-Type: application/json\n\n'
                '%s') % (outdoor.get_current_data())

    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
