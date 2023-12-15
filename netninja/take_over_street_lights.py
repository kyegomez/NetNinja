import requests


def find_and_access_street_lights(ip_range):
    for i in range(1, 255):
        ip = f"{ip_range}.{i}"
        try:
            response = requests.get(
                f"http://{ip}/status", timeout=0.5
            )
            if response.status_code == 200:
                print(
                    f"Street light found at {ip}, status:"
                    f" {response.text}"
                )
        except requests.exceptions.RequestException:
            pass  # No device at this IP or it didn't respond in time


# Usage
find_and_access_street_lights("192.168.1")
