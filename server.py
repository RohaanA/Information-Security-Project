''' 
+------------------------------------------------------------------------------+
| server.py                                                                    |
|                                                                              |
| Project: IPSec VPN Tunnel w/ Multiphase Encryption                           |
| Authors: Rohaan, Ahmed Moiz, Zubair Fawad                                    |
| Version: 1.0                                                                 |
|                                                                              |
| Description: This file contains the server side code for the VPN tunnel.     |
|                                                                              |
| Notes:                                                                       |
+------------------------------------------------------------------------------+
| This project uses the IPSec VPN tunneling protocol to establish a secure     |
| connection between two hosts. The protocol is implemented in Python.         |
|                                                                              |
| The protocol consists of 3 phases:                                           |
| 1. IKE Phase 1: Main Mode                                                    |
| 2. IKE Phase 2: Quick Mode                                                   |
| 3. IPSec Phase: Encrypted Data Transfer                                      |
|                                                                              |
| The protocol uses the following encryption algorithms:                       |
| 1. Diffie-Hellman Key Exchange                                               |
| 2. RSA Public Key Encryption                                                 |
| 3. AES Encryption                                                            |
|                                                                              |
| The protocol uses the following hashing algorithms:                          |
| 1. SHA-256                                                                   |
| 2. SHA-512                                                                   |
+------------------------------------------------------------------------------+

'''
import socket
from utils import server_log
import signal


# Global variable
keep_running = True
def shutdown_server(signal, frame):
    global keep_running
    print("Shutting down the server...")
    keep_running = False
# Register the signal function handler
signal.signal(signal.SIGINT, shutdown_server)
class Server:
    def __init__(self, port):
        self.port = port
        
        print("Server side code")
        pass
    pass

    def printDetails(self):
        server_log("--------------------", "warning")
        server_log("Printing Server Details")
        server_log("Port: " + str(self.port))
        server_log("--------------------", "warning")
        pass
    def startServer(self):
        global keep_running
        # Open socket on given self.port.
        server_log("Opening socket on port " + str(self.port))
        server_address = ('localhost', self.port)  # Replace with the desired server address
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_address)
        # Listen for incoming connections.
        server_socket.listen(1)
        while keep_running:
            # Accept incoming connections.
            pass
        
        server_socket.close()
        server_log("Server stopped.", "warning")
        # Receive data from client.
        
        # Decrypt data.
        
        
        
        pass

# Start server side code
def server():
    port = 6000
    
    server = Server(port)
    #Printing current server details
    server.printDetails()
    server.startServer()
    pass


if __name__ == '__main__':
    server()