import os
import subprocess
import sys
import time
from threading import Thread
from itertools import cycle
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ASCII Banner
BANNER = f"""{Fore.LIGHTCYAN_EX}
 █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗
██╔══██╗████╗  ██║██╔════╝ ████╗  ██║
███████║██╔██╗ ██║██║  ███╗██╔██╗ ██║
██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║
██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝
{Style.RESET_ALL}"""

# Loading spinner
def spinner(task_description):
    """Show a loading spinner during long tasks."""
    done = False
    spinner_cycle = cycle(["|", "/", "-", "\\"])
    def spinning():
        while not done:
            sys.stdout.write(f"\r{Fore.LIGHTCYAN_EX}[INFO] {task_description}... {next(spinner_cycle)}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
    Thread(target=spinning).start()
    return lambda: setattr(locals(), "done", True)

# Utility Functions
def run_command(command, description, silent=False):
    """Run a shell command with a spinner."""
    spinner_stop = spinner(description)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        spinner_stop()
        print(f"\r{Fore.LIGHTGREEN_EX}[INFO] {description}... Done!{Style.RESET_ALL}")
        if not silent:
            print(result.stdout.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        spinner_stop()
        print(f"\r{Fore.RED}[ERROR] {description} failed: {e.stderr.strip()}{Style.RESET_ALL}")
        sys.exit(1)

def check_root():
    """Ensure the script is run as root."""
    if os.geteuid() != 0:
        print(f"{Fore.RED}[ERROR] This script must be run as root!{Style.RESET_ALL}")
        sys.exit(1)

# MAC Spoofing
def spoof_mac(interface, interval=None):
    """Spoof the MAC address."""
    if interval:
        print(f"{Fore.LIGHTGREEN_EX}[INFO] Changing MAC address every {interval} minutes.{Style.RESET_ALL}")
        while True:
            change_mac(interface)
            time.sleep(interval * 60)
    else:
        change_mac(interface)

def change_mac(interface):
    """Change the MAC address once."""
    print(f"{Fore.LIGHTCYAN_EX}[INFO] Changing MAC address for {interface}.{Style.RESET_ALL}")
    run_command(["ifconfig", interface, "down"], "Bringing interface down")
    run_command(["macchanger", "-r", interface], "Randomizing MAC address")
    run_command(["ifconfig", interface, "up"], "Bringing interface up")

# Features
def install_dependencies():
    """Install required tools."""
    dependencies = ["tor", "proxychains4", "macchanger"]
    run_command(["apt-get", "update"], "Updating package list")
    run_command(["apt-get", "install", "-y"] + dependencies, "Installing dependencies")

def configure_tor_proxychains():
    """Set up Tor and Proxychains."""
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Configuring Tor and Proxychains...{Style.RESET_ALL}")
    torrc_path = "/etc/tor/torrc"
    proxychains_config = "/etc/proxychains4.conf"

    # Configure Tor
    if "SocksPort 9050" not in open(torrc_path).read():
        with open(torrc_path, "a") as f:
            f.write("\n# Enable SOCKS proxy\nSocksPort 9050\n")

    # Configure Proxychains
    with open(proxychains_config, "r+") as f:
        content = f.read()
        if "socks5 127.0.0.1 9050" not in content:
            f.write("\nsocks5 127.0.0.1 9050\n")

    run_command(["systemctl", "restart", "tor"], "Restarting Tor service")

def anonymity_test():
    """Test anonymity using a public IP check."""
    try:
        ip = run_command(["proxychains4", "curl", "-s", "ifconfig.me"], "Checking public IP")
        print(f"{Fore.LIGHTCYAN_EX}[INFO] Your anonymized IP is: {ip}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Anonymity test failed: {e}{Style.RESET_ALL}")

# Menu
def menu():
    """Display the main menu."""
    print(BANNER)
    print(f"{Fore.LIGHTGREEN_EX}Welcome to ANON!{Style.RESET_ALL}")
    print("""
    1. Install Dependencies
    2. Configure Tor and Proxychains
    3. Test Anonymity
    4. Spoof MAC Address
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
            interface = input(f"{Fore.LIGHTCYAN_EX}Enter interface (e.g., eth0): {Style.RESET_ALL}")
            interval = input(f"{Fore.LIGHTCYAN_EX}Enter interval in minutes (leave blank to change once): {Style.RESET_ALL}")
            if interval:
                spoof_mac(interface, int(interval))
            else:
                spoof_mac(interface)
        elif choice == "5":
            print(f"{Fore.LIGHTGREEN_EX}Exiting ANON. Stay secure!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}[ERROR] Invalid choice. Try again!{Style.RESET_ALL}")

if __name__ == "__main__":
    check_root()
    menu()
