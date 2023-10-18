import pywifi
import time  # Needed for sleep
from pywifi import const  # If needed for status definitions

class NetworkScanner:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()

    def scan(self):
        iface = self.wifi.interfaces()[0]
        iface.scan()
        results = iface.scan_results()
        networks = []

        for network in results:
            networks.append({
                'SSID': network.ssid,
                'BSSID': network.bssid,
                'Security': 'WPA' if pywifi.const.AKM_TYPE_WPA in network.akm else 'Open'  # Simplified, you may want to expand this
            })

        return networks
