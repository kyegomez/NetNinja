from scapy.all import ARP, Ether, srp

def scan_network(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for sent, received in answered_list:
        clients_list.append({'ip': received.psrc, 'mac': received.hwsrc})

    return clients_list

# replace '192.168.1.1/24' with your network
clients_list = scan_network("192.168.1.1/24")
for client in clients_list:
    print(f"IP Address: {client['ip']} - MAC Address: {client['mac']}")