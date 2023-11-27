import platform
import random
import subprocess

class NetworkScanner:
    def _rank_network(self, network):
        # Max points for each component
        max_signal_points = 30
        max_ssid_points = 20
        signal_divisor = 100.0  # Pre-computed value for signal strength calculation

        # Security Scoring
        security_scores = {'WPA3': 50, 'WPA2': 35, 'WPA': 25, 'WEP': 15, 'OPEN': 5}
        security = network.get('Authentication', '').upper()
        security_score = security_scores.get(security, 0)

        # Signal Strength Scoring
        signal_strength = int(network.get('Signal', '0%').rstrip('%'))
        signal_score = min(signal_strength / signal_divisor * max_signal_points, max_signal_points)

        # SSID Analysis Scoring
        common_ssids = ['default', 'linksys', 'netgear', 'xfinity']
        ssid_score = max_ssid_points - 10 if any(common_name in network['SSID'].lower() for common_name in common_ssids) else max_ssid_points

        # Total Score
        total_score = min(security_score + signal_score + ssid_score, 100)  # Ensure score doesn't exceed 100

        network['Score'] = round(total_score, 2)  # Round the score for better readability
        return network

    def _parse_network_data(self, raw_data):
        networks = []
        current_network = {}
        for line in raw_data.split('\n'):
            line = line.strip()
            if line.startswith("SSID"):
                if current_network:
                    self._rank_network(current_network)
                    networks.append(current_network)
                    current_network = {}
                ssid = line.split(':', 1)[1].strip()
                current_network['SSID'] = ssid
            elif line.startswith("BSSID"):
                bssid = line.split(':', 1)[1].strip()
                current_network['BSSID'] = bssid
            elif line.startswith("Signal"):
                signal = line.split(':', 1)[1].strip()
                current_network['Signal'] = signal
            elif line.startswith("Authentication"):
                auth = line.split(':', 1)[1].strip()
                current_network['Authentication'] = auth

        if current_network:
            self._rank_network(current_network)
            networks.append(current_network)
        return networks
    
    
    def _get_fake_network_data(self):
        fake_networks = []
        for _ in range(10):
            signal = f"{random.randint(20, 100)}%"
            auth_options = ['WPA3', 'WPA2', 'WPA', 'WEP', 'OPEN']
            fake_networks.append({
                'SSID': f"Network_{random.randint(1, 100)}",
                'BSSID': ':'.join('%02x' % random.randint(0, 255) for _ in range(6)),
                'Signal': signal,
                'Authentication': random.choice(auth_options)
            })
        return '\n'.join([f"SSID: {net['SSID']}\nBSSID: {net['BSSID']}\nSignal: {net['Signal']}\nAuthentication: {net['Authentication']}" for net in fake_networks])

    def scan(self):
        networks_raw = ''
        if platform.system() == 'Windows':
            try:
                process = subprocess.Popen(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                networks_raw, error = process.communicate(timeout=30)
                if process.returncode != 0:
                    print(f"Command failed with error: {error}")
                    return []
            except subprocess.TimeoutExpired:
                print("Scanning process timed out.")
                return []
        else:
            networks_raw = self._get_fake_network_data()

        parsed_networks = self._parse_network_data(networks_raw)
        ranked_networks = [self._rank_network(network) for network in parsed_networks]
        ranked_networks.sort(key=lambda x: x['Score'], reverse=True)
        # Return only the top 10 networks
        top_networks = ranked_networks[:10]
        return top_networks