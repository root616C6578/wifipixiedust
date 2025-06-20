import subprocess
import shlex

def monitor_up(interface):
    #Commands
    ifdown = f"sudo ifconfig {interface} down"
    iwconfig = f"sudo iwconfig {interface} mode monitor"
    ifup = f"sudo ifconfig {interface} up"

    # Enable monitor mode
    subprocess.call(shlex.split(ifdown))
    subprocess.call(shlex.split(iwconfig))
    subprocess.call(shlex.split(ifup))