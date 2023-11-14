import subprocess

class NetworkScanner:
    def _rank_network(self, network):
        # Max points for each component
        max_security_points = 50
        max_signal_points = 30
        max_ssid_points = 20

        # Security Scoring
        security_scores = {'WPA3': 50, 'WPA2': 35, 'WPA': 25, 'WEP': 15, 'OPEN': 5}
        security = network.get('Authentication', '').upper()
        security_score = security_scores.get(security, 0)

        # Signal Strength Scoring
        signal_strength = int(network.get('Signal', '0%').rstrip('%'))
        signal_score = min(signal_strength / 100 * max_signal_points, max_signal_points)

        # SSID Analysis Scoring
        ssid_score = max_ssid_points
        if any(common_name in network['SSID'].lower() for common_name in ['default', 'linksys', 'netgear', 'xfinity']):
            ssid_score -= 10  # Deduct points for common SSID names

        # Total Score
        total_score = security_score + signal_score + ssid_score
        total_score = min(total_score, 100)  # Ensure score doesn't exceed 100

        network['Score'] = round(total_score, 2)  # Round the score for better readability
        return network
    def scan(self):
        # Run the 'netsh wlan show networks' command
    # Try running the 'netsh wlan show networks' command and handle potential errors
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'], capture_output=True, text=True, check=True)
            networks_raw = result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            return []

        networks = []
        current_network = {}

        # Parse the command output
        for line in networks_raw.split('\n'):
            line = line.strip()  # Remove any leading/trailing whitespace
            if line.startswith("SSID"):
                # When we find a new SSID, save the previous one (if any)
                if current_network:
                    # Rank the network before appending
                    self._rank_network(current_network)
                    networks.append(current_network)
                    current_network = {}
                # Extract the SSID
                ssid = line.split(':', 1)[1].strip()
                current_network['SSID'] = ssid
            elif line.startswith("BSSID"):
                # Extract the BSSID (MAC address)
                bssid = line.split(':', 1)[1].strip()
                current_network['BSSID'] = bssid
            elif line.startswith("Signal"):
                # Extract the Signal strength
                signal = line.split(':', 1)[1].strip()
                current_network['Signal'] = signal
            elif line.startswith("Authentication"):
                # Extract the Authentication type
                auth = line.split(':', 1)[1].strip()
                current_network['Authentication'] = auth

        # Don't forget to add the last network when done
        if current_network:
            self._rank_network(current_network)
            networks.append(current_network)

        # Sort networks based on the score
        networks.sort(key=lambda x: x['Score'], reverse=True)
        return networks