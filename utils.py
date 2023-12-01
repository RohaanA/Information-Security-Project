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
    # Define the connection type based on the use_https flag
    conn_type = "http" if not use_https else "https"
    
    try:
        # Establish a connection to the specified site and port
        conn = http.client.HTTPConnection(site, port) if not use_https else http.client.HTTPSConnection(site, port)
        
        # Send an HTTP GET request
        conn.request("GET", "/")
        
        # Get the HTTP response
        response = conn.getresponse()
        
        # Get the HTTP response headers
        headers = response.getheaders()
        
        # Get the HTTP response body
        body = response.read()
        
        # Close the connection
        conn.close()
        
        # Return the generated HTTP packet
        return {
            "method": "GET",
            "url": f"{conn_type}://{site}:{port}/",
            "headers": headers,
            "body": body
        }
    except http.client.HTTPException as e:
        # Handle any exceptions that occur during the request
        print("An error occurred:", e)