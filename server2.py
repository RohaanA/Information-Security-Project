import socket
import ssl

# Server configuration
server_host = '0.0.0.0'
server_port = 8000
certfile = '/path/to/server_cert.pem'
keyfile = '/path/to/server_key.pem'

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((server_host, server_port))

# Listen for incoming connections
server_socket.listen(1)

print('Server listening on {}:{}'.format(server_host, server_port))

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(client_address[0], client_address[1]))

    # Wrap the client socket with an SSL/TLS context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)

    # Receive data from the client
    received_data = ssl_socket.recv(1024)
    print('Received data from client:', received_data)

    # Send a response back to the client
    response = 'Hello, client!'
    ssl_socket.send(response.encode())

    # Close the SSL/TLS connection
    ssl_socket.close()

# Close the server socket
server_socket.close()