import socket
import ipaddress


def get_local_ip():
    """
    Get the local IP address of the current machine.

    Returns:
    str: The local IP address.
    """
    try:
        # This creates a dummy socket to connect to an external address
        # The local IP address is determined by the socket's choice of interface to reach the external address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(
            ("8.8.8.8", 80)
        )  # Google's DNS as the external address
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def get_lan_network(ip_address):
    """
    Calculate the LAN network range based on the IP address.

    Args:
    ip_address (str): The local IP address of the device.

    Returns:
    str: LAN network range in CIDR notation.
    """
    try:
        # Assuming a common subnet mask for typical home/office networks (255.255.255.0)
        # For different setups, this subnet mask might need to be adjusted
        network = ipaddress.ip_network(
            f"{ip_address}/24", strict=False
        )
        return str(network)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


# Using the Functions
local_ip = get_local_ip()
if local_ip:
    print(f"Local IP Address: {local_ip}")
    lan_network = get_lan_network(local_ip)
    if lan_network:
        print(f"LAN Network: {lan_network}")
