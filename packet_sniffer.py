from scapy.all import *

def packet_handler(packet):
    # Process and analyze the captured packet here
    print(packet.summary())

# Set the Wi-Fi interface to capture packets on
interface = "Intel(R) Wi-Fi 6E AX211 160MHz"  # Replace with your Wi-Fi interface name

# Set the capture filter to capture Wi-Fi traffic only
capture_filter = "wlan"

# Start capturing Wi-Fi packets
sniff(iface=interface, prn=packet_handler, filter=capture_filter)
