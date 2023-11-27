import socket
import signal
import threading
import select
import ssl
from utils import server_log

# Global variable
keep_running = True

def shutdown_server(signal, frame):
    global keep_running
    print("Shutting down the server...")
    keep_running = False

class Server:
    def __init__(self, port):
        self.port = port

    def printDetails(self):
        server_log("--------------------", "warning")
        server_log("Printing Server Details")
        server_log("Port: " + str(self.port))
        server_log("--------------------", "warning")

    def _handle_client(self, client_socket, client_address):
        server_log("[CLIENT HANDLER] Client connected: {}:{}".format(*client_address), "success")
        # Handle client communication here

    def startServer(self):
        global keep_running
        # Open socket on given self.port.
        certfile = '/etc/letsencrypt/live/rohaan.xyz/fullchain.pem'
        keyfile = '/etc/letsencrypt/live/rohaan.xyz/privkey.pem'
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile, keyfile)
        server_log("Opening socket on port " + str(self.port))
        server_address = ('0.0.0.0', self.port)
        server_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_side=True)
        server_socket.bind(server_address)
        server_socket.listen(1)

        # Make the server socket non-blocking
        server_socket.setblocking(False)

        # Create a list of sockets to monitor for activity
        sockets = [server_socket]

        while keep_running:
            try:
                # Use select to monitor sockets for activity
                readable, _, _ = select.select(sockets, [], [], 0.1)

                for sock in readable:
                    if sock is server_socket:
                        # Accept new client connection
                        client_socket, client_address = server_socket.accept()
                        # Add the new client socket to the list of sockets
                        sockets.append(client_socket)
                        # Start a new thread to handle the client
                        threading.Thread(target=self._handle_client, args=(client_socket, client_address)).start()

                    else:
                        # Handle client communication
                        # Check if a Keyboard interrupt has been received
                        if not keep_running:
                            break

            except KeyboardInterrupt:
                # Keyboard interrupt received, stop the server
                print("Keyboard interrupt received. Shutting down the server...")
                keep_running = False
                break

        # Close all client sockets
        for sock in sockets[1:]:
            sock.close()

        # Close the server socket
        server_socket.close()

        server_log("Server stopped.", "warning")

# Start server side code
def server():
    port = 443

    server = Server(port)
    # Printing current server details
    server.printDetails()
    server.startServer()

if __name__ == '__main__':
    server()