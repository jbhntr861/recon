#!/bin/bash

# Set up USB tethering interface
sudo ifconfig usb0 up
sudo dhclient usb0

# Set up IP forwarding
echo "Enabling IP forwarding..."
sudo sysctl -w net.ipv4.ip_forward=1

# Set up NAT for USB tethering interface
echo "Configuring NAT..."
sudo iptables --table nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i usb0 -o wlan0 -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o usb0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Set default gateway to USB tethering interface
echo "Setting default gateway to USB tethering..."
sudo ip route del default
sudo ip route add default via $(ip addr show usb0 | grep 'inet ' | awk '{print $2}' | cut -f1 -d'/')

echo "USB tethering set up complete."
