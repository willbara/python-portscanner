# Remember to merge cli stack in cpp later

import socket # importing socket library to communicate at low level
import threading # adding multithreading to speed up scanning process
import ssl # for https connections
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

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
def scan_port(ip, port, open_ports, result_box): # scan_port takes two parameters here
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            # socket.socket() creates a new socket object
            # AF_INET specifies we want to use an IPv4 address
            # SOCK_STREAM specifies we're using TCP
            # with statement makes sure that it closes automatically after use
            s.settimeout(1) # closes after 1 second of connection attempt before moving on
            # connect_ex attempts connection, if it succeeds, return 0
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
                service_name = PORT_SERVICES.get(port, "Unknown Service")
                result_box.insert(tk.END, f"Port {port} ({service_name}): {banner.strip()[:100]}\n")

    except Exception as e:
        result_box.insert(tk.END, f"Error scanning port {port}: {e}\n")

# function to scan multiple ports using threads
def scan_ports(ip, ports, result_box):
    open_ports = []
    threads = []

    for port in ports:
        # threading.Thread() creates a new thread
        # target=scan_port is what function the thread will run
        # target= and args= tells the function what to do/look for
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports, result_box))
        # add thread to our list
        threads.append(thread)
        thread.start()
    # wait for threads to finish
    for thread in threads:
        thread.join()

    if not open_ports:
        result_box.insert(tk.END, f"No open ports found on {ip}.\n")
    result_box.insert(tk.END, "\nScan complete.\n")

# start scan when button is clicked
def start_scan(ip_entry, result_box):
    ip = ip_entry.get()
    ports = range(1, 1024)  # default port range

    if not ip:
        messagebox.showerror("Input Error", "Please enter a valid IP address.")
        return

    result_box.delete(1.0, tk.END)  # Clear previous results
    threading.Thread(target=scan_ports, args=(ip, ports, result_box)).start()

# main GUI setup
def main():
    root = tk.Tk()
    root.title("Port Scanner with Banner Grabbing")
    root.geometry("600x500")

    # IP Address Entry
    ttk.Label(root, text="Target IP Address:").pack(pady=5)
    ip_entry = ttk.Entry(root, width=40)
    ip_entry.pack(pady=5)

    # Scan Button
    scan_button = ttk.Button(root, text="Start Scan", command=lambda: start_scan(ip_entry, result_box))
    scan_button.pack(pady=10)

    # Results Display (ScrolledText)
    result_box = scrolledtext.ScrolledText(root, width=70, height=20)
    result_box.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()