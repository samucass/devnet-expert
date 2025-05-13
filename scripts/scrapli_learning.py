from scrapli.driver.core import NXOSDriver, IOSXEDriver
from pprint import pprint

router1 = {
    "host": "192.168.1.133",
    "auth_username": "admin",
    "auth_password": "cisco123",
    "auth_strict_key": False,
}

router2 = {
    "host": "192.168.1.154",
    "auth_username": "admin",
    "auth_password": "cisco123",
    "auth_secondary": "cisco123",
    "auth_strict_key": False,
}

def main():
    """Simple example demonstrating getting structured data via textfsm/ntc-templates"""
    with NXOSDriver(**router1) as conn:
        # Platform drivers will auto-magically handle disabling paging for you
        result = conn.send_command("show version")

    #print(result.result)
    #pprint(result.genie_parse_output())
    device_version1 = result.genie_parse_output()
    print(device_version1["platform"]["os"])
    print(device_version1["platform"]["software"]["system_version"])

    with IOSXEDriver(**router2) as conn:
        # Platform drivers will auto-magically handle disabling paging for you
        result = conn.send_command("show version")

    #print(result.result)
    #pprint(result.genie_parse_output())
    device_version2 = result.genie_parse_output()
    print(device_version2["version"]["os"])
    print(device_version2["version"]["version"])

    # 'show vlan' example
    # vlans = result.genie_parse_output()
    # pprint(vlans["vlans"]["10"]["interfaces"][0])

    # 'show version' example
    # device_version = result.genie_parse_output()
    # print(device_version["version"]["os"])

if __name__ == "__main__":
    main()

#conn = NXOSDriver(**router1)
#conn.open()
#response = conn.send_command("show version")
#print(f"=== NX-OS Device ({router1['host']}) ===")
#print(response.result)
#
#conn = IOSXEDriver(**router2)
#conn.open()
#response = conn.send_command("show version")
#print(f"\n=== IOS Device ({router2['host']}) ===")
#print(response.result)
