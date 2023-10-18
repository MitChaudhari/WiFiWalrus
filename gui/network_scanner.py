import pywifi
import time  # Needed for sleep
from pywifi import const  # If needed for status definitions

class NetworkScanner:
    def __init__(self):
        pass  # Or initialize anything you need here

    def scan(self):
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]  # You may want to select an interface based on certain criteria

        iface.scan()  # Triggers scanning the network
        time.sleep(8)  # Scanning may take a while, this delay allows for that

        scan_results = iface.scan_results()
        
        networks = []
        for network in scan_results:
            ssid = network.ssid
            bssid = network.bssid
            # The 'akm' field contains security information, but it's a list of security protocols
            # It might be not straightforward and require processing to make this information user-friendly
            security = network.akm  

            network_info = {
                'SSID': ssid,
                'BSSID': bssid,  # You can include this if it's needed in your table
                'Security': security,  # This will be a list; you might need further processing
                # Add other network details here
            }
            networks.append(network_info)

        return networks
