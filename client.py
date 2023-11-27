import socket
import ssl
from utils import client_log

vpn_host = "rohaan.xyz"
vpn_port = 443

def start_connection():
    client_log("Beginning connection to VPN Server: " + vpn_host + ":" + str(vpn_port))
    
    # Create a socket object
    s = socket.socket()
    
    # Create a client-side SSL/TLS context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Connect to the VPN server using SSL/TLS
    ssl_sock = context.wrap_socket(s, server_hostname=vpn_host)
    ssl_sock.connect((vpn_host, vpn_port))
    
    # Send/receive data over the SSL/TLS connection as needed
    # ssl_sock.send(b"Hello, Server!")
    # response = ssl_sock.recv(1024)
    
    # Close the SSL/TLS connection
    ssl_sock.close()

if __name__ == '__main__':
    start_connection()