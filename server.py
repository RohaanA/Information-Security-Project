import socket
import threading
import select
from utils import server_log
import ssl
import logger
import requests

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

    def _generate_packet_from_request(self, request_data):
        # Decoding the request_data
        request_data = request_data.decode()
        
        # Splitting the request_data into lines
        lines = request_data.split('\r\n')
        
        # Extracting the method, path, and protocol from the first line
        method, path, protocol = lines[0].split(' ')
        
        # Extracting the host and port from the subsequent lines
        host = None
        port = None
        
        for line in lines[1:]:
            if line.startswith('Host:'):
                host_with_port = line.split(': ')[1]
                if ':' in host_with_port:
                    host, port = host_with_port.split(':')
                    port = int(port)
                else:
                    host = host_with_port
                    port = 80  # Default port if not specified
                break
        
        # Generating the request packet
        packet = f"{method} {path} {protocol}\r\n"
        packet += f"Host: {host}\r\n"
        packet += "Connection: close\r\n"  # Adding Connection header
        packet += "\r\n"
        
        return packet, host, port
        
        return packet, host, port
    def _handle_client(self, client_socket, ssl_socket, client_address):
        #Setup the logger
        logger_instance = logger.Logger()
        #Create a log file for the client
        logger_instance.create_log_file("client_" + str(client_address[0]) + "_" + str(client_address[1]) + ".log")
        
        server_log("[CLIENT HANDLER] Client connected: {}:{}".format(*client_address), "success", logger_instance)
            # Receive data from the client
        received_data = ssl_socket.recv(1024)
        # print('Received data from client:', received_data)
        packet,host,port = self._generate_packet_from_request(received_data)
        
        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.connect((host, int(port)))
        print(packet)
        destination_socket.send(packet.encode())

        # Receive the response from the destination in a loop until no more data is received
        response = b''
        while True:
            data = destination_socket.recv(1024)
            if not data:
                break
            response += data

        # Print the response
        decoded_response = response.decode()
        print(decoded_response)
        
        # Using requests to get the html content of the website (host + port)
        response = requests.get("http://" + host + ":" + str(port))
        html_content = response.text
        # Send a response back to the client
        # response = 'Hello, client!'
        # ssl_socket.send(decoded_response.encode())
        ssl_socket.send(html_content.encode())

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
                        try:
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
                        except ssl.SSLError:
                            print('SSL/TLS handshake failed. Closing connection.')
                            client_socket.close()

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
    port = 80

    server = Server(port)
    # Printing current server details
    server.printDetails()
    server.startServer()

if __name__ == '__main__':
    server()