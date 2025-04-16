from models.enums import DeviceType


class Device:
    def __init__(self, id, url, device_type: DeviceType, alert_yellow: float, alert_orange: float, alert_red: float):
        if not isinstance(device_type, DeviceType):
            raise ValueError("device_type must be an instance of DeviceType enum")
        self.id = id
        self.type = device_type
        self.url = url
        self.yellow = float(alert_yellow)
        self.orange = float(alert_orange)
        self.red = float(alert_red)

class DeviceList:
    def __init__(self):
        self.devices = []

    def add_device(self, device: Device):
        self.devices.append(device)

    def delete_device(self, device: Device):
        self.devices.remove(device)

    def set_devices(self, devices: list):
        self.devices = devices
