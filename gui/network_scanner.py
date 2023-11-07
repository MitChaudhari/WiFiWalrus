import pywifi
from pywifi import const, Profile
class NetworkScanner:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]
    
    def _rank_network(self, network):
        # Initial score
        score = 0

        # Adjust score based on security type
        security = network.get('Authentication', '').upper()
        if 'WPA3' in security:
            score += 100
        elif 'WPA2' in security:
            score += 70
        elif 'WPA' in security:
            score += 50
        elif 'WEP' in security:
            score += 30
        # Assuming open networks have 'Open' in the security type
        elif 'OPEN' in security:
            score += 10

        # Adjust score based on signal strength
        # Assuming the signal strength is a percentage value
        # If signal is not in percentage, this needs to be adjusted
        signal_strength = int(network.get('Signal', '0%').rstrip('%'))
        score += signal_strength

        # Deduct score for common/default SSID names
        ssid = network['SSID'].lower()
        if any(common_name in ssid for common_name in ['default', 'linksys', 'netgear', 'xfinity']):
            score -= 20

        # Save the score in the network dictionary
        network['Score'] = score
        return network

    def scan(self):
        self.iface.scan()
        scan_results = self.iface.scan_results()

        networks = []
        for network in scan_results:
            ssid = network.ssid
            bssid = network.bssid
            signal_strength = network.signal

            # Convert signal strength to a percentage (this is an approximation)
            # The actual conversion from dBm to percentage can vary
            signal_percent = min(max(2 * (signal_strength + 100), 0), 100)

            # Determine security type
            security = self._determine_security(network)

            current_network = {
                'SSID': ssid,
                'BSSID': bssid,
                'Signal': f'{signal_percent}%',
                'Authentication': security,
            }

            self._rank_network(current_network)
            networks.append(current_network)

        networks.sort(key=lambda x: x['Score'], reverse=True)
        return networks

    def _determine_security(self, network):
        # This is a simplified way to determine the security type
        # You may need to expand this method to handle different security types properly
        if network.akm == []:
            security = 'OPEN'
        elif const.AKM_TYPE_WPA2PSK in network.akm:
            security = 'WPA2'
        elif const.AKM_TYPE_WPAPSK in network.akm:
            security = 'WPA'
        elif const.AKM_TYPE_WPA3PSK in network.akm:
            security = 'WPA3'
        else:
            security = 'OTHER'

        return security

# Example usage:
if __name__ == "__main__":
    scanner = NetworkScanner()
    ranked_networks = scanner.scan()
    for network in ranked_networks:
        print(network)