import http.client
#This function is used to log the server messages (color coded: red for errors, green for success, yellow for warnings, blue for info)
color_codes = {
        "error": '\033[91m',
        "success": '\033[92m',
        "warning": '\033[93m',
        "info": '\033[94m'
}
#This function is called to log the server messages
def server_log(message, type="info", logger=None):
    color_code = color_codes.get(type, color_codes.get("info"))
    print(color_code + "[SERVER] " + message + '\033[0m')
    if logger:
        logger.log(message)
def client_log(message, type="info", log_text=None):
    color_code = color_codes.get(type, color_codes.get("info"))
    print(color_code + "[CLIENT] " + message + '\033[0m')
    
#This function generates packet to connect to 


def generate_http_packet(site, port, use_https=False):
    method = 'GET'
    path = '/'
    protocol = 'HTTP/1.1'
    
    if use_https:
        protocol = 'HTTPS/1.1'
    
    packet = f"{method} {path} {protocol}\r\n"
    packet += f"Host: {site}\r\n"
    packet += f"Port: {port}\r\n"
    packet += "Connection: close\r\n"
    packet += "\r\n"
    
    return packet