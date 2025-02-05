# Remember to merge cli stack in cpp later
# importing socket library to communicate at low level
import socket

# using scan_port function to check single point
def scan_port(ip, port): # scan_port takes two parameters here
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            # socket.socket() creates a new socket obkect
            # AF_INET specifies we want to use an IPv4 address
            # SOCK_STREAM specifies we're using TCP
            # with statement makes sure that it closes automatically after use
            s.settimeout(1) # closes after 1 second of connection attempt before moving on
            # connect_ex attmepts connection, if it succeeds, return 0
            result = s.connect_ex((ip, port))
            if result == 0:
                return True
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    return False

def scan_ports(ip, ports):
    # creating a list to store open ports
    open_ports = []
    # loop through each port
    for port in ports:
        # For each port, scan_port() is called to check if its open
        if scan_port(ip, port):
            # if port is open, its added to open_ports list
            open_ports.append(port)
    # returns list of open ports
    return open_ports

if __name__ == "__main__":
    target_ip = input("Enter the IP address to scan: ")
    ports_to_scan = range(1, 1025)
    # calls the scan_ports() function to scan range of inputted IP
    open_ports = scan_ports(target_ip, ports_to_scan)

    if open_ports:
        print(f"Open ports on {target_ip}: {open_ports}")
    else:
        print(f"No open ports found on {target_ip}")