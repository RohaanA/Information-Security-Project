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
    
    packet = f"{method} {path} {protocol}\r\n"
    packet += f"Host: {site}\r\n"
    packet += f"Port: {port}\r\n"
    packet += "Connection: close\r\n"
    packet += "\r\n"
    
    return packet

def extract_new_location(response):
    headers, body = response.split('\r\n\r\n', 1)  # Split the response into headers and body
    lines = headers.split('\r\n')  # Split the headers into lines
    for line in lines:
        if line.startswith('Location: '):
            return line.split('Location: ')[1]  # Extract the new location
    return None
def check_whitelist(IP):
    with open("credentials/whitelist.txt", "r") as file:
        for line in file:
            if line.strip() == IP:
                return True
    return False