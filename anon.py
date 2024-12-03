import os
import subprocess
import sys
from time import sleep
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ASCII Banner
BANNER = f"""{Fore.LIGHTCYAN_EX}
 █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗██╗   ██╗███╗   ██╗██╗   ██╗███████╗███████╗██████╗ 
██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██║   ██║████╗  ██║██║   ██║██╔════╝██╔════╝██╔══██╗
███████║██╔██╗ ██║██║  ███╗██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║█████╗  █████╗  ██║  ██║
██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██╔══╝  ██║  ██║
██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝███████╗███████╗██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═════╝ 
{Style.RESET_ALL}
"""


# Utility Functions
def run_command(command, description, silent=False):
    """Run a shell command and display description."""
    print(f"{Fore.LIGHTGREEN_EX}[INFO] {description}{Style.RESET_ALL}")
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        if not silent:
            print(f"{Fore.LIGHTCYAN_EX}{result.stdout.strip()}{Style.RESET_ALL}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[ERROR] {e.stderr.strip()}{Style.RESET_ALL}")
        sys.exit(1)


def check_root():
    """Ensure the script is run as root."""
    if os.geteuid() != 0:
        print(f"{Fore.RED}[ERROR] This script must be run as root!{Style.RESET_ALL}")
        sys.exit(1)


# Features
def install_dependencies():
    """Install required tools."""
    dependencies = ["tor", "proxychains4", "openssh-client", "tcpdump", "nmap"]
    run_command(["sudo", "apt-get", "update"], "Updating package list...")
    run_command(["sudo", "apt-get", "install", "-y"] + dependencies, "Installing dependencies...")


def configure_tor_proxychains():
    """Set up Tor and Proxychains."""
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Configuring Tor and Proxychains...{Style.RESET_ALL}")
    torrc_path = "/etc/tor/torrc"
    proxychains_config = "/etc/proxychains4.conf"

    # Configure Tor
    with open(torrc_path, "a") as f:
        if "SocksPort 9050" not in open(torrc_path).read():
            f.write("\n# Enable SOCKS proxy\nSocksPort 9050\n")

    # Configure Proxychains
    with open(proxychains_config, "r+") as f:
        content = f.read()
        if "socks5 127.0.0.1 9050" not in content:
            f.write("\nsocks5 127.0.0.1 9050\n")

    run_command(["sudo", "systemctl", "restart", "tor"], "Restarting Tor service...")


def anonymity_test():
    """Test anonymity using a public IP check."""
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Testing anonymity...{Style.RESET_ALL}")
    try:
        ip = run_command(["proxychains4", "curl", "-s", "ifconfig.me"], "Checking public IP...")
        print(f"{Fore.LIGHTCYAN_EX}[INFO] Your anonymized IP is: {ip}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Anonymity test failed: {e}{Style.RESET_ALL}")


def advanced_features():
    """Run advanced features like network monitoring."""
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Starting advanced features...{Style.RESET_ALL}")
    print("1. Scan Network with Nmap")
    print("2. Monitor Traffic with Tcpdump")
    choice = input(f"{Fore.LIGHTCYAN_EX}Choose an option: {Style.RESET_ALL}")

    if choice == "1":
        target = input(f"{Fore.LIGHTCYAN_EX}Enter target IP/subnet for Nmap: {Style.RESET_ALL}")
        run_command(["sudo", "nmap", "-A", target], f"Scanning network {target}...")
    elif choice == "2":
        interface = input(f"{Fore.LIGHTCYAN_EX}Enter network interface (e.g., eth0): {Style.RESET_ALL}")
        run_command(["sudo", "tcpdump", "-i", interface], f"Monitoring traffic on {interface}...")


# Main Menu
def menu():
    """Display the main menu."""
    print(BANNER)
    print(f"{Fore.LIGHTGREEN_EX}Welcome to Anonmyzer!{Style.RESET_ALL}")
    print("""
    1. Install Dependencies
    2. Configure Tor and Proxychains
    3. Test Anonymity
    4. Advanced Features
    5. Exit
    """)
    while True:
        choice = input(f"{Fore.LIGHTCYAN_EX}Choose an option: {Style.RESET_ALL}")
        if choice == "1":
            install_dependencies()
        elif choice == "2":
            configure_tor_proxychains()
        elif choice == "3":
            anonymity_test()
        elif choice == "4":
            advanced_features()
        elif choice == "5":
            print(f"{Fore.LIGHTGREEN_EX}Exiting Anonmyzer. Stay anonymous!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}[ERROR] Invalid choice. Try again!{Style.RESET_ALL}")


if __name__ == "__main__":
    check_root()
    menu()
