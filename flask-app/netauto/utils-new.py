from scrapli.driver.core import IOSXEDriver, NXOSDriver
from pprint import pprint
from config import inv

def get_version(hostname: str) -> None:
    print(f"\n🔍 Processing device: {hostname}")

    dev = inv.get(hostname)
    if not dev:
        print(f"❌ Device '{hostname}' not found in inventory.")
        return

    device_type = dev.get("device_type")
    if device_type == "iosxe":
        driver = IOSXEDriver
        #transport = "paramiko"
    elif device_type == "nxos":
        driver = NXOSDriver
        #transport = "ssh2"
    else:
        print(f"❌ Unsupported device type for '{hostname}'.")
        return

    my_device = {
        "host": dev.get("host"),
        "auth_username": dev.get("user"),
        "auth_password": dev.get("pass"),
        "auth_strict_key": False,
        "timeout_socket": 5,
        "timeout_transport": 5,
        "ssh_config_file": "~/.ssh/config"  # IMPORTANT: Full path to user config
        #"transport": "paramiko",  # Enforce paramiko for all devices (esp. for old SSH)
        #"transport": transport
    }

    # Only add enable password if it's present (IOS only)
    if dev.get("enable_pass"):
        my_device["auth_secondary"] = dev.get("enable_pass")

    try:
        print(f"🚀 Connecting to {hostname}...")
        #print("Using SSH config file:", my_device.get("ssh_config_file")) ### DEBUG
        #print("Using transport:", my_device.get("transport")) ### DEBUG
        
        with driver(**my_device) as conn:
            print("✅ Connected. Sending command...")
            result = conn.send_command("show version")
            parsed_output = result.genie_parse_output()

            # Extract and print software version
            if device_type == "iosxe":
                ios_version = parsed_output["version"]["version"]
                print(f"🖥️ {hostname} Software Version: {ios_version}")
            elif device_type == "nxos":
                #nxos_version = parsed_output["platform"]["software"]["kickstart_version"]
                nxos_version = parsed_output["platform"]["software"]["system_version"]
                print(f"🖥️ {hostname} Software Version: {nxos_version}")
    
    except Exception as e:
        print(f"❌ Exception occurred on {hostname}: {e}")

# Test all devices
if __name__ == "__main__":
    for device in ["R1", "N9K", "N7K", "N5K"]:
        get_version(device)