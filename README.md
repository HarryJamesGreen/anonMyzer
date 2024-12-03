Project Title: Anonmyzer

Table of Contents:
- Project Overview
- Features
- Setup Instructions
- Usage Guide
- Technical Details
- Future Improvements
- Contributors
- License

---

Project Overview:
Anonmyzer is a Python-based tool designed to enhance online anonymity by leveraging technologies like Tor, Proxychains, and SSH tunneling. It provides a user-friendly CLI interface to configure, test, and utilize these tools for routing internet traffic securely.

This project is part of a university assignment focusing on cybersecurity, privacy, and advanced networking concepts.

---

Features:
- Tor Integration: Automatically configures and starts Tor for anonymous routing.
- Proxychains Support: Routes commands through a proxy chain for added security.
- SSH Tunneling: Allows dynamic SOCKS proxy creation via remote SSH servers.
- Anonymity Testing: Verifies the anonymity level by checking the public IP address.
- Interactive CLI: Step-by-step instructions for ease of use.

---

Setup Instructions:
Follow these steps to set up and run Anonmyzer:

Prerequisites:
1. Operating System: Linux-based system (tested on Ubuntu/Kali).
2. Python: Version 3.7 or higher.
3. Packages: Ensure "tor", "proxychains4", and "openssh-client" are installed.

Installation:
1. Clone the repository:
   git clone https://github.com/your-username/anonmyzer.git
   cd anonmyzer
2. Run the script as root:
   sudo python3 anonmyzer.py

---

Usage Guide:
1. Install Dependencies: Option 1 in the menu installs required tools.
2. Configure Anonymity Tools: Option 2 sets up Tor and Proxychains.
3. Set Up SSH Tunnel: Option 3 creates an SSH-based SOCKS proxy.
4. Test Anonymity: Option 4 checks your public IP through the proxy chain.
5. Run Commands Anonymously: Option 5 allows executing custom commands anonymously.

---

Technical Details:
1. Tor: Routes traffic through multiple encrypted relays, hiding your IP address.
2. Proxychains: Redirects application traffic through the Tor SOCKS proxy.
3. SSH Tunneling: Adds an extra layer of anonymity by routing traffic through a compromised or trusted server.
4. Python Modules Used:
   - os and subprocess: For system interactions and command execution.
   - sys: For error handling and script control.

---

Future Improvements:
- DNS Leak Prevention: Integrate checks to ensure DNS requests are anonymized.
- Multi-hop Proxies: Implement support for multiple chained proxies.
- Automated Log Cleanup: Add functionality to wipe temporary logs and traces.
- Graphical User Interface: Provide a GUI version for less technical users.

---

Contributors:
- Harry Green: Project Lead and Developer
  BSc Cybersecurity and Forensics (3rd Year)

---

License:
This project is licensed under the MIT License. See LICENSE file for details.
