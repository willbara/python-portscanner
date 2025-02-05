# Remember to merge cli stack in cpp later

import socket # importing socket library to communicate at low level
import threading # adding multithreading to speed up scanning process
import ssl # for https connections

# dictionary for common ports
PORT_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
    853: "DNS over TLS"
}

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
                banner = ''
                # attempt to grab a banner after connection
                try:
                    if port == 443:
                        context = ssl.create_default_context()
                        with context.wrap_socket(s, server_hostname=ip) as ssock:
                            ssock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')
                            banner = ssock.recv(1024).decode('utf-8', errors='ignore')
                    else: 
                        # sends an HTTP HEAD request to prompt a response from web servers
                        s.sendall(b'HEAD / HTTP/1.0\r\n\r\n') # For http/s ports
                        # reads up to 1024 bytes of data from the socket and decodes into a string
                        banner = s.recv(1024).decode('utf-8', errors='ignore') # get response
                except:
                    banner = "No banner received"
                # stores the port number and banner into a tuple (python class mentioned wooooow)
                open_ports.append((port, banner.strip())) # store port and banner info

    except Exception as e:
        print(f"Error scanning port {port}: {e}")

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
    open_ports = scan_ports(target_ip, ports_to_scan)

    if open_ports:
        print(f"\nOpen ports and banners on {target_ip}:\n")
        for port, banner in open_ports:
            service_name = PORT_SERVICES.get(port, "Unknown Service")
            banner_display = banner if banner else 'No banner received'
            # Limiting banner output to first 200 characters for readability
            print(f"Port {port} ({service_name}): {banner_display[:200]}{'...' if len(banner_display) > 200 else ''}")
    else:
        print(f"No open ports found on {target_ip}.")