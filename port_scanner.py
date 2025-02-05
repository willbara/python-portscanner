# Remember to merge cli stack in cpp later

import socket # importing socket library to communicate at low level
import threading # adding multithreading to speed up scanning process
import ssl # for https connections
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ipaddress # for handling IP ranges

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
def scan_port(ip, port, open_ports, result_box, progress_bar, total_ports): # scan_port takes two parameters here
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
    finally:
        progress_bar.step(1 / total_ports * 100) # update progress bar

# function to scan multiple ports using threads
def scan_ports(ip, ports, result_box, progress_bar):
    open_ports = []
    threads = []
    total_ports = len(ports)

    for port in ports:
        # threading.Thread() creates a new thread
        # target=scan_port is what function the thread will run
        # target= and args= tells the function what to do/look for
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports, result_box, progress_bar, total_ports))
        # add thread to our list
        threads.append(thread)
        thread.start()
    # wait for threads to finish
    for thread in threads:
        thread.join()

    if not open_ports:
        result_box.insert(tk.END, f"No open ports found on {ip}.\n")
    result_box.insert(tk.END, "\nScan complete.\n")
    progress_bar.pack_forget() # hide progress bar after scan

# start scan when button is clicked
def start_scan(ip_entry, end_ip_entry, start_port_entry, end_port_entry, result_box, progress_bar):
    start_ip = ip_entry.get()
    end_ip = end_ip_entry.get()

    # validate IP addresses
    try:
        start_ip_obj = ipaddress.IPv4Address(start_ip)
        if end_ip:
            end_ip_obj = ipaddress.IPv4Address(end_ip)
            if start_ip_obj > end_ip_obj:
                messagebox.showerror("Input Error", "Start IP must be less than or equal to End IP.")
                return
            ip_range = [str(ip) for ip in ipaddress.summarize_address_range(start_ip_obj, end_ip_obj)]
        else:
            ip_range = [start_ip]
    except ipaddress.AddressValueError:
        messagebox.showerror("Input Error", "Please enter valid IP addresses.")
        return

    # validate port range
    try:
        start_port = int(start_port_entry.get()) if start_port_entry.get() else 1
        end_port = int(end_port_entry.get()) if end_port_entry.get() else 1024
        if start_port > end_port:
            messagebox.showerror("Input Error", "Start port must be less than or equal to End port.")
            return
        ports = range(start_port, end_port + 1)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port numbers.")
        return

    result_box.delete(1.0, tk.END)  # Clear previous results
    progress_bar.pack(pady=5)  # Show progress bar
    progress_bar['value'] = 0  # Reset progress bar

    # scan each IP in the range
    for ip in ip_range:
        result_box.insert(tk.END, f"\nScanning {ip}...\n")
        threading.Thread(target=scan_ports, args=(ip, ports, result_box, progress_bar)).start()

# main GUI setup
def main():
    root = tk.Tk()
    root.title("Banner Scanner")
    root.geometry("600x600")

    # Apply color scheme
    style = ttk.Style(root)
    style.theme_use('clam')  # Use 'clam' theme as base

    # General window background
    root.configure(bg="#2e2e2e")

    # Customize Label appearance
    style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Arial", 10))

    # Customize Entry fields to remove white borders
    style.configure("TEntry", 
                    fieldbackground="#3e3e3e",  # Background color of entry fields
                    foreground="#ffffff",       # Text color
                    bordercolor="#2e2e2e",      # Border color to match background
                    relief="flat",              # Flat border style for cleaner look
                    padding=5)                  # Slight padding for better spacing

    # Customize Button appearance to remove white borders
    style.configure("TButton", 
                    background="#4e4e4e", 
                    foreground="#ffffff",
                    bordercolor="#2e2e2e",      # Match border with background
                    relief="flat",              # Flat border style
                    padding=5)

    # Customize Progress Bar
    style.configure("TProgressbar", background="#007acc")

    # Customize Frame background to match the theme
    style.configure("TFrame", background="#2e2e2e")

    # Customize ScrolledText (non-ttk, so configure separately)
    result_box_bg = "#1e1e1e"
    result_box_fg = "#d4d4d4"

    # IP Address Entry
    ttk.Label(root, text="Start IP Address:").pack(pady=5)
    ip_entry = ttk.Entry(root, width=40)
    ip_entry.pack(pady=5)

    ttk.Label(root, text="End IP Address (leave blank to scan a single IP):").pack(pady=5)
    end_ip_entry = ttk.Entry(root, width=40)
    end_ip_entry.pack(pady=5)

    # Port Range Entries
    port_frame = ttk.Frame(root)
    port_frame.pack(pady=5)

    ttk.Label(port_frame, text="Start Port:").grid(row=0, column=0, padx=5)
    start_port_entry = ttk.Entry(port_frame, width=10)
    start_port_entry.insert(0, "1")
    start_port_entry.grid(row=0, column=1, padx=5)

    ttk.Label(port_frame, text="End Port:").grid(row=0, column=2, padx=5)
    end_port_entry = ttk.Entry(port_frame, width=10)
    end_port_entry.insert(0, "1024")
    end_port_entry.grid(row=0, column=3, padx=5)

    # Scan Button
    scan_button = ttk.Button(root, text="Start Scan", command=lambda: start_scan(ip_entry, end_ip_entry, start_port_entry, end_port_entry, result_box, progress_bar))
    scan_button.pack(pady=10)

    # Results Display (ScrolledText)
    result_box = scrolledtext.ScrolledText(root, width=70, height=20, bg=result_box_bg, fg=result_box_fg, insertbackground="white")
    result_box.pack(pady=10)

    # Progress Bar (hidden initially)
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")

    root.mainloop()

if __name__ == "__main__":
    main()