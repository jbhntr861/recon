import os
import subprocess

class DHCP:
    def __init__(self, interface, ip_address, subnet_mask, start_ip, end_ip):
        self.interface = interface
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.start_ip = start_ip
        self.end_ip = end_ip

    def configure_dnsmasq(self):
        dnsmasq_config = f"""
interface={self.interface}
dhcp-range={self.start_ip},{self.end_ip},{self.subnet_mask},12h
dhcp-option=3,{self.ip_address}
dhcp-option=6,8.8.8.8,8.8.4.4
        """
        with open("/etc/dnsmasq.conf", "w") as dnsmasq_config_file:
            dnsmasq_config_file.write(dnsmasq_config)

        subprocess.run(["systemctl", "restart", "dnsmasq"], check=True)
