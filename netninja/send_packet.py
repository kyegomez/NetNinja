from scapy.all import IP, ICMP, send


def send_packet(destination_ip):
    """
    Send an ICMP echo request (ping) to a specified IP address.

    Args:
    destination_ip (str): The IP address of the destination device.
    """
    packet = IP(dst=destination_ip) / ICMP()
    send(packet)


#

for i in range(10000000):
    out = send_packet()
    print(out)
