import socket
import signal
import threading
import select
from utils import server_log
import ssl

# Global variable
keep_running = True

def shutdown_server(signal, frame):
    global keep_running
    print("Shutting down the server...")
    keep_running = False

class Server:
    def __init__(self, port):
        self._port = port
        self._host = "0.0.0.0"
        self._certfile = '/etc/letsencrypt/live/rohaan.xyz/fullchain.pem'
        self._keyfile = '/etc/letsencrypt/live/rohaan.xyz/privkey.pem'

    def printDetails(self):
        server_log("--------------------", "warning")
        server_log("Printing Server Details")
        server_log("Port: " + str(self._port))
        server_log("Host: " + str(self._host))
        server_log("--------------------", "warning")

    def _handle_client(self, client_socket, ssl_socket, client_address):
        server_log("[CLIENT HANDLER] Client connected: {}:{}".format(*client_address), "success")
            # Receive data from the client
        received_data = ssl_socket.recv(1024)
        print('Received data from client:', received_data)
        # Send a response back to the client
        response = 'Hello, client!'
        ssl_socket.send(response.encode())

        # Close the SSL/TLS connection
        ssl_socket.close()
        client_socket.close()

    def startServer(self):
        global keep_running
        # Open socket on given self.port.
        server_log("Opening socket on port " + str(self._port))
        server_address = ('0.0.0.0', self._port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_address)
        server_socket.listen(1)
        print('Server listening on {}:{}'.format(self._host, self._port))
        
        # Make the server socket non-blocking
        server_socket.setblocking(False)

        # Create a list of sockets to monitor for activity
        sockets = [server_socket]

        while keep_running:
            try:
                try:
                # Use select to monitor sockets for activity
                    readable, _, _ = select.select(sockets, [], [], 0.1)
                except select.error:
                    # Raised when one of the monitored sockets is closed
                    # So remove it from the list of sockets we're monitoring
                    for sock in sockets:
                        if sock.fileno() == -1:
                            sockets.remove(sock)
                    continue

                for sock in readable:
                    if sock.fileno() == -1:
                        # Socket is closed, remove it from the list
                        sockets.remove(sock)
                        continue
                    if sock is server_socket:
                        # Accept new client connection
                        client_socket, client_address = server_socket.accept()
                        print('Accepted connection from {}:{}'.format(client_address[0], client_address[1]))
                        # Wrap the client socket with an SSL/TLS context
                        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                        print(self._certfile)
                        print(self._keyfile)
                        ssl_context.load_cert_chain(certfile=self._certfile, keyfile=self._keyfile)
                        ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)
                        # Add the new client socket to the list of sockets
                        sockets.append(ssl_socket)
                        # Start a new thread to handle the client
                        threading.Thread(target=self._handle_client, args=(client_socket, ssl_socket, client_address)).start()

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