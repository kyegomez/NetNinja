import requests
import socket
import scapy.all as scapy


def get_all_device_data(ip_range):
    """
    Get all data about all devices on a LAN network.

    Args:
    ip_range (str): IP address or range (e.g., '192.168.1.0/24')

    Returns:
    list: List of dictionaries containing device data.
    """
    devices = []

    # Scan the network
    answered_list = scapy.arping(ip_range)

    for element in answered_list[0]:
        device = {}
        device["ip"] = element[1].psrc
        device["mac"] = element[1].hwsrc

        # Get the hostname
        try:
            device["hostname"] = socket.gethostbyaddr(device["ip"])[0]
        except socket.herror:
            device["hostname"] = "Unknown"

        # Get the device type
        device["type"] = get_device_type(device["mac"])

        # Add other data as needed
        # ...

        devices.append(device)

    return devices


def get_device_type(mac_address):
    """
    Get the device type based on the MAC address.

    Args:
    mac_address (str): MAC address of the device.

    Returns:
    str: Device type.
    """
    # Send a GET request to the MAC Vendors API
    response = requests.get(
        f"https://api.macvendors.com/{mac_address}"
    )

    # If the request was successful, return the vendor name
    if response.status_code == 200:
        return response.text

    # If the request was not successful, return "Unknown"
    return "Unknown"
