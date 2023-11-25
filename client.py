import socket
from utils import client_log
#
vpn_host = "vpn.rohaan.xyz"
vpn_port = 443
def start_connection():
    client_log("Beginning connection to VPN Server: " + vpn_host + ":" + str(vpn_port))
    # Create a socket object
    s = socket.socket()
    # Connect to vpn server
    s.connect((vpn_host, vpn_port))
    
    
if __name__ == '__main__':
    start_connection()