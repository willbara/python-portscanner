# Remember to merge cli stack in cpp later
# importing socket library to communicate at low level
import socket
# adding multithreading to speed up scanning process
import threading

# using scan_port function to check single point
def scan_port(ip, port, open_ports): # scan_port takes two parameters here
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
                open_ports.append(port) # actually add the ports to list
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    return False

def scan_ports(ip, ports):
    # creating empty lists to store ports and threads for processing
    open_ports = []
    threads = []

    for port in ports:
        # threading.Thread() creates a new thread
        # target=scan_port is what function the thread will run
        # target= and args= tells the function what to do/look for
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        # add thread to our list
        threads.append(thread)
        thread.start()
    # wait for threads to finish
    for thread in threads:
        thread.join()
    
    return open_ports

if __name__ == "__main__":
    target_ip = input("Enter the IP address to scan: ")
    ports_to_scan = range(1, 1024)
    # calls the scan_ports() function to scan range of inputted IP
    open_ports = scan_ports(target_ip, ports_to_scan)

    if open_ports:
        print(f"Open ports on {target_ip}: {open_ports}")
    else:
        print(f"No open ports found on {target_ip}")