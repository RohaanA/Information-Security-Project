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
http_packet = generate_http_packet("www.google.com", 80, use_https=False)

# data = 'Hello, server!'
# ssl_socket.send(data.encode())

print(http_packet)
ssl_socket.send(http_packet.encode())

# Receive a response from the server
response = ssl_socket.recv(131072)
print('Received response from server:', response.decode())

# Save the received data to an HTML file
with open("received.html", "wb") as file:
    file.write(response)

# Open the file in a web browser
import webbrowser
webbrowser.open("received.html")

# Close the SSL/TLS connection
ssl_socket.close()