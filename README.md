# Port Scanner with Banner Grabbing

A **Python-based Port Scanner** with a basic **Tkinter GUI** that can scan a single IP address or rang, to detect open ports, and grab banners from services. The scanner includes features like multithreading for speed, service detection, custom port ranges, and a progress bar that updates in real-time.

---

## Screenshot
![Port Scanner GUI](path_to_screenshot.png)

## Features

- **Scan Single IP or IP Range**: Input one IP or scan across multiple devices on your network.
- **Custom Port Range Selection**: Specify the start and end ports or use the default range (1-1024).
- **Banner Grabbing**: Identify running services and their banners (e.g., HTTP headers).
- **Progress Bar**: Visual progress indicator that hides after scan completion.
- **Multithreaded Scanning**: Fast and efficient port scanning using Python's threading module.
- **Dark Mode GUI**: A clean, modern interface with dark theme aesthetics.

---

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/your-username/port-scanner.git
    cd port-scanner
    ```

2. **Set Up a Virtual Environment** *(optional but recommended)*:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Libraries**:

    The script uses standard Python libraries, but ensure **Tkinter** is installed (comes pre-installed with most Python versions).

---

## Usage

1. **Run the Script**:

    ```bash
    python port_scanner.py
    ```

2. **Using the GUI**:
    - Enter the **Start IP Address**.
    - (Optional) Enter the **End IP Address** to scan a range.
    - Specify the **Start Port** and **End Port** *(defaults to 1-1024)*.
    - Click **Start Scan** to begin.
    - View results in the output box, with open ports and banner information.

---

## Example Output

```
Scanning 192.168.0.1...
Port 22 (SSH): OpenSSH 7.6p1 Ubuntu-4ubuntu0.3
Port 80 (HTTP): HTTP/1.1 200 OK
Server: Apache/2.4.29 (Ubuntu)

Scan complete.
```

---

## Contribution

Feel free to fork this repository and submit pull requests for improvements,


## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- Inspired by **Nmap** and other network scanning tools.
- [Python](https://www.python.org/)
- [tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Cryptography Library](https://cryptography.io/)

---