#!/bin/bash

# Install necessary packages
sudo apt update
sudo apt install -y kea-dhcp4-server isc-dhcp-server dnsmasq

# Stop any running DHCP servers
sudo service isc-dhcp-server stop
sudo service dnsmasq stop

# Configure kea-dhcp4-server
sudo cp /etc/kea/kea-dhcp4.conf.sample /etc/kea/kea-dhcp4.conf
sudo sed -i 's/option domain-name-servers 8.8.8.8, 8.8.4.4;/option domain-name-servers 192.168.1.1;/g' /etc/kea/kea-dhcp4.conf
sudo sed -i 's/option routers 192.168.1.1;/option routers 192.168.1.1;\n  subnet4 192.168.1.0\/24 {\n    pool4 192.168.1.10 - 192.168.1.250;\n    option routers 192.168.1.1;\n    option domain-name-servers 192.168.1.1;\n  }/g' /etc/kea/kea-dhcp4.conf

# Configure dnsmasq
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak
sudo touch /etc/dnsmasq.conf
sudo echo "interface=lo" | sudo tee -a /etc/dnsmasq.conf
sudo echo "dhcp-range=192.168.1.10,192.168.1.250,12h" | sudo tee -a /etc/dnsmasq.conf
sudo echo "dhcp-option=3,192.168.1.1" | sudo tee -a /etc/dnsmasq.conf
sudo echo "dhcp-option=6,192.168.1.1" | sudo tee -a /etc/dnsmasq.conf

# Start kea-dhcp4-server and dnsmasq
sudo service kea-dhcp4-server start
sudo service dnsmasq start

echo "DHCP servers successfully set up."
