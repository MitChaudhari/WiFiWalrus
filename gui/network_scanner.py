import subprocess

class NetworkScanner:
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
    
# Example of how we might use this class:
if __name__ == "__main__":
    scanner = NetworkScanner()
    ranked_networks = scanner.scan()
    for network in ranked_networks:
        print(network)