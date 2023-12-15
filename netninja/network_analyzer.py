from scapy.all import sniff, IP, TCP


class NetworkAnalyzer:
    def __init__(
        self, interface="eth0", packet_filter="ip", count=10
    ):
        self.interface = interface
        self.packet_filter = packet_filter
        self.count = count

    def packet_callback(self, packet):
        if packet.haslayer(IP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            print(
                f"IP Packet: {ip_src} is sending a packet to {ip_dst}"
            )

        if packet.haslayer(TCP):
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            print(
                f"TCP Packet: {tcp_sport} is sending a packet to"
                f" {tcp_dport}"
            )

    def start_sniffing(self):
        sniff(
            iface=self.interface,
            filter=self.packet_filter,
            count=self.count,
            prn=self.packet_callback,
        )


# Usage
analyzer = NetworkAnalyzer(
    interface="eth0", packet_filter="ip", count=100
)
analyzer.start_sniffing()
