import requests
import hashlib
from requests.exceptions import RequestException

class DatabaseManager:
    API_ENDPOINT = "http://ec2-3-140-116-49.us-east-2.compute.amazonaws.com:8000/frontendAPI/"

    @staticmethod
    def calculate_hash(ssid, bssid):
        data = f"{ssid}{bssid}".encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def send_to_api(self, networks):
        for network in networks:
            ssid = network['SSID']
            bssid = network['BSSID']
            authentication = network.get('Authentication', 'N/A')
            signal = network.get('Signal', 'N/A')
            score = round(network.get('Score', 0))  # Round score to nearest integer
            network_hash = self.calculate_hash(ssid, bssid)

            # Prepare data to send to API
            network_data = {
                "ssid": ssid,
                "bssid": bssid,
                "authType": authentication,
                "signalStrength": signal,
                "connectionScore": score,
                "networkHash": network_hash
            }
            try:
                response = requests.post(
                    self.API_ENDPOINT,
                    json=network_data,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 201:
                    print(f"Successfully sent data for network {ssid}")
                else:
                    print(f"Error sending data for network {ssid}: {response.status_code}")
                    print(response.text)

            except RequestException as e:
                print(f"Failed to send data for network {ssid}. Error: {e}")

# Example usage for testing purposes
if __name__ == "__main__":
    db_manager = DatabaseManager()
    sample_networks = [
        {'SSID': 'TestNetwork1', 'BSSID': '00:11:22:33:44:55', 'Authentication': 'WPA2', 'Signal': '70%', 'Score': 80},
        {'SSID': 'TestNetwork2', 'BSSID': '11:22:33:44:55:66', 'Authentication': 'WPA', 'Signal': '50%', 'Score': 70},
    ]
    db_manager.send_to_api(sample_networks)
