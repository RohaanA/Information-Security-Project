import socket
import ssl

# Server configuration
server_host = 'vpn.rohaan.xyz'
server_port = 443
certfile = 'certs/client_cert.pem'
keyfile = 'certs/client_key.pem'

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the client socket with an SSL/TLS context
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=server_host)

# Connect to the server
ssl_socket.connect((server_host, server_port))

# Send data to the server
data = 'Hello, server!'
ssl_socket.send(data.encode())

# Receive a response from the server
response = ssl_socket.recv(1024)
print('Received response from server:', response.decode())

# Close the SSL/TLS connection
ssl_socket.close()