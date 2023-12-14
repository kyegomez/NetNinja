import argparse
import logging
from scapy.all import sniff


def setup_logger():
    """
    Set up logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def packet_callback(packet):
    """
    Callback function that gets called for each captured packet.
    """
    logging.info(packet.summary())


def capture_traffic(interface):
    """
    Capture traffic on the specified network interface.

    Args:
    interface (str): Name of the network interface to capture traffic on.
    """
    try:
        logging.info(f"Starting packet capture on {interface}...")
        sniff(iface=interface, prn=packet_callback, store=False)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Network Packet Sniffer"
    )
    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        required=True,
        help="Network interface to capture traffic on",
    )
    args = parser.parse_args()

    capture_traffic(args.interface)


if __name__ == "__main__":
    setup_logger()
    main()
