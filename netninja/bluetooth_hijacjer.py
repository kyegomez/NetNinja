import bluetooth


def find_bluetooth_devices():
    """Find  nearby Bluetooth devices.
    """
    print("Searching for Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        try:
            print("Device: {}, {}".format(name, addr))
        except UnicodeEncodeError:
            print(
                "Device: {} - {}".format(
                    addr, name.encode("utf-8", "replace")
                )
            )


find_bluetooth_devices()    
