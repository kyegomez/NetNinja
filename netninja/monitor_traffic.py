import socket
import struct
from fastapi import FastAPI
from threading import Thread

app = FastAPI()


def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", data[:14])
    return (
        get_mac_addr(dest_mac),
        get_mac_addr(src_mac),
        socket.htons(proto),
        data[14:],
    )


def get_mac_addr(bytes_addr):
    bytes_str = map("{:02x}".format, bytes_addr)
    return ":".join(bytes_str).upper()


def monitor_traffic(interface):
    with socket.socket(
        socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)
    ) as s:
        s.bind((interface, 0))
        while True:
            raw_data, addr = s.recvfrom(65535)
            dest_mac, src_mac, eth_proto, data = ethernet_frame(
                raw_data
            )
            print("\nEthernet Frame:")
            print(
                "Destination: {}, Source: {}, Protocol: {}".format(
                    dest_mac, src_mac, eth_proto
                )
            )


@app.get("/start_monitoring/{interface}")
def start_monitoring(interface: str):
    Thread(target=monitor_traffic, args=(interface,)).start()
    return {"message": f"Started monitoring on interface {interface}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
