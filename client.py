import socket
import ssl
from utils import generate_http_packet

# Server configuration
server_host = 'vpn.rohaan.xyz'
server_port = 80
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

# Generating an HTTP packet for google.com on port 80
http_packet = generate_http_packet("google.com", 80, use_https=False)
# Convert the HTTP packet into a properly formatted HTTP request
request = f"{http_packet['method']} {http_packet['url']} HTTP/1.1\r\n"
headers = "\r\n".join([f"{header[0]}: {header[1]}" for header in http_packet['headers']])
request += headers + "\r\n\r\n"

# data = 'Hello, server!'
# ssl_socket.send(data.encode())

print(request)
ssl_socket.send(request.encode())

# Receive a response from the server
response = ssl_socket.recv(1024)
print('Received response from server:', response.decode())

# Close the SSL/TLS connection
ssl_socket.close()