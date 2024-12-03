import os
import subprocess
import sys
import time

# === Utility Functions ===

def run_command(command, silent=False):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if not silent:
            print(result.stdout.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command '{' '.join(command)}' failed: {e.stderr.strip()}")
        sys.exit(1)

def check_root():
    """Ensure the script is run as root."""
    if os.geteuid() != 0:
        print("[ERROR] This script must be run as root.")
        sys.exit(1)

# === Core Features ===

def install_dependencies():
    """Install Tor, Proxychains, and OpenSSH."""
    print("[INFO] Installing dependencies...")
    dependencies = ["tor", "proxychains4", "openssh-client"]
    run_command(["sudo", "apt-get", "update"])
    run_command(["sudo", "apt-get", "install", "-y"] + dependencies)
    print("[INFO] Dependencies installed.")

def configure_tor():
    """Set up Tor configuration."""
    print("[INFO] Configuring Tor...")
    torrc_path = "/etc/tor/torrc"
    with open(torrc_path, "a") as f:
        if "SocksPort 9050" not in open(torrc_path).read():
            f.write("\n# Enable SOCKS proxy\nSocksPort 9050\n")
    run_command(["sudo", "systemctl", "restart", "tor"])
    print("[INFO] Tor configured and restarted.")

def configure_proxychains():
    """Set up Proxychains to use Tor."""
    print("[INFO] Configuring Proxychains...")
    proxychains_config = "/etc/proxychains4.conf"
    with open(proxychains_config, "r+") as f:
        content = f.read()
        if "socks5 127.0.0.1 9050" not in content:
            f.write("\nsocks5 127.0.0.1 9050\n")
    print("[INFO] Proxychains configured.")

def start_tor():
    """Ensure Tor is running."""
    print("[INFO] Starting Tor service...")
    run_command(["sudo", "systemctl", "start", "tor"])
    print("[INFO] Tor service started.")

def setup_ssh_tunnel(remote_host, remote_user, remote_port=22):
    """Create an SSH tunnel for dynamic SOCKS proxying."""
    print(f"[INFO] Setting up SSH tunnel to {remote_host}:{remote_port}...")
    ssh_command = ["ssh", "-fN", "-D", "8080", f"{remote_user}@{remote_host}", "-p", str(remote_port)]
    run_command(ssh_command)
    print("[INFO] SSH tunnel established on localhost:8080.")

def test_anonymity():
    """Test anonymity using a public IP check."""
    print("[INFO] Testing anonymity...")
    try:
        response = run_command(["proxychains4", "curl", "-s", "ifconfig.me"])
        print(f"[INFO] Public IP (via Tor/Proxy): {response}")
    except Exception as e:
        print("[ERROR] Anonymity test failed:", str(e))

def run_anon_command():
    """Run a user-provided command through Proxychains."""
    command = input("Enter the command to run anonymously: ").split()
    try:
        run_command(["proxychains4"] + command)
    except Exception as e:
        print("[ERROR] Failed to run command anonymously:", str(e))

# === User Interface ===

def menu():
    """Display the menu and handle user input."""
    print("""
    === Anonmyzer Menu ===
    1. Install Dependencies
    2. Configure Tor and Proxychains
    3. Set up SSH Tunnel
    4. Test Anonymity
    5. Run Anonymous Command
    6. Exit
    """)
    while True:
        try:
            choice = int(input("Choose an option: "))
            if choice == 1:
                install_dependencies()
            elif choice == 2:
                configure_tor()
                configure_proxychains()
                start_tor()
            elif choice == 3:
                remote_host = input("Enter remote host (e.g., 192.168.1.1): ")
                remote_user = input("Enter remote SSH username: ")
                remote_port = input("Enter remote SSH port (default 22): ") or 22
                setup_ssh_tunnel(remote_host, remote_user, int(remote_port))
            elif choice == 4:
                test_anonymity()
            elif choice == 5:
                run_anon_command()
            elif choice == 6:
                print("Exiting...")
                break
            else:
                print("[ERROR] Invalid option. Please try again.")
        except ValueError:
            print("[ERROR] Please enter a number.")

# === Entry Point ===

if __name__ == "__main__":
    check_root()
    menu()
