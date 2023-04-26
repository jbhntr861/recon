import re
import subprocess

class AccessPoint:
    def get_monitor_mode_interface(self):
        result = subprocess.run(["sudo", "airmon-ng"], capture_output=True, text=True)
        output = result.stdout
        pattern = re.compile(r"(\w+mon|\w+mon\d+)")
        match = pattern.search(output)

        return match.group(0) if match else None

    def setup_access_point(self, interface, essid="Xnitity", channel=6):
        subprocess.run(["sudo", "airbase-ng", "-e", essid, "-c", str(channel), "-v", interface])

    def setup_bridge_and_dhcp(self, interface):
        subprocess.run(["sudo", "brctl", "addbr", "br0"])
        subprocess.run(["sudo", "ifconfig", "br0", "192.168.1.1", "netmask", "255.255.255.0"])
        subprocess.run(["sudo", "brctl", "addif", "br0", interface])
        subprocess.run(["sudo", "ifconfig", "br0", "up"])
        subprocess.run(["sudo", "service", "isc-dhcp-server", "stop"])
        subprocess.run(["sudo", "echo", 'INTERFACESv4="br0"', ">", "/etc/default/isc-dhcp-server"])
        subprocess.run(["sudo", "service", "isc-dhcp-server", "start"])

class HTTrack:
    def download_webpage(self, url, output_directory):
        subprocess.run(["httrack", url, "-O", output_directory, "+*.example.com/*"])

    def setup_captive_portal(self, html_file_path):
        subprocess.run(["sudo", "cp", "-R", html_file_path, "/etc/nodogsplash/htdocs/"])
        subprocess.run(["sudo", "sed", "-i", f"s|SplashPage .*|SplashPage {html_file_path}|", "/etc/nodogsplash/nodogsplash.conf"])
        subprocess.run(["sudo", "service", "nodogsplash", "restart"])
