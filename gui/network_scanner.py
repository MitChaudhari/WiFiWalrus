import subprocess
import re
from scapy.sendrecv import sniff
from scapy.layers.dot11 import Dot11
from scapy.layers.dot11 import Dot11Elt, Dot11EltCountry, Dot11EltRates, Dot11EltVendorSpecific
import hashlib
import pywifi
from pywifi import const

class NetworkScanner:
    def __init__(self):
        pass

    def scan(self):
        self.networks_data = []
        input_file = "sample.cap"
        sniff(offline=input_file, prn=self._collect_network_data)
        return self.networks_data

    def _collect_network_data(self, frame):
        if frame.haslayer(Dot11) and frame.type == 0 and frame.subtype == 8:
            ssid = frame.info.decode('utf-8', errors='ignore')
            bssid = frame.addr3
            channel = int(ord(frame[Dot11Elt:3].info))
            
            if frame.haslayer(Dot11EltCountry):
                country = frame[Dot11EltCountry].country_string.decode('utf-8', errors='ignore')
            else:
                country = "Unknown"
            
            security = self._determine_security(frame)  # using scanner_proto.py logic
            score = self._calculate_score(security)  # new function to calculate score
            recommendation = self._get_recommendation(score)  # new function to determine recommendation

            network_data = {
                'SSID': ssid,
                'Security': security,
                'Score': score,
                'Recommendation': recommendation,
                'Detail': f"BSSID: {bssid}, Channel: {channel}, Country: {country}"  
            }

            self.networks_data.append(network_data)

    def _determine_security(self, frame):
        # For the sake of the example, we're just using WPA2 and WPA. You should extend this for all security types.
        if frame.haslayer(Dot11Elt) and frame.ID == 48:  
            return "WPA2-PSK"
        else:
            return "Unknown"

    def _calculate_score(self, security):
        # Basic scoring mechanism based on security type
        scores = {
            "WPA2-PSK": 90,
            "WPA2": 85,
            "WPA-PSK": 80,
            "WPA": 75,
            "WEP": 50,
            "Open": 20,
            "Unknown": 0
        }
        return scores.get(security, 0)

    def _get_recommendation(self, score):
        # Providing recommendations based on score
        if score > 80:
            return "Excellent"
        elif 60 < score <= 80:
            return "Good"
        elif 40 < score <= 60:
            return "Average"
        else:
            return "Poor"
        
    def _parse_result(self, result):
        # This function is retained from your previous structure for potential use with airodump-ng.
        networks = []
        lines = result.split('\n')
        for line in lines[2:]:
            details = re.split(r'\s+', line.strip())
            if len(details) > 4:
                networks.append({
                    'SSID': details[0],
                    'Security': details[3],
                    'Score': details[4],
                    'Recommendation': 'Safe',
                    'Detail': details[5],
                })
        return networks