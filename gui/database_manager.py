import mysql.connector
from hashlib import sha256

# Database connection parameters
db_config = {
    'user': 'root',
    'password': 'ipro497db',
    'host': 'ec2-3-12-150-224.us-east-2.compute.amazonaws.com',
    'database': 'ipro1'
}
class DatabaseManager:
    def __init__(self):
        self.db_config = db_config

    @staticmethod
    def calculate_hash(ssid, bssid):
        data = f"{ssid}{bssid}".encode("utf-8")
        return sha256(data).hexdigest()

    def send_to_database(self, networks):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            insert_query = "INSERT INTO connections (SSID, BSSID, Authentication, Signal, Score, SHA256_Hash) VALUES (%s, %s, %s, %s, %s, %s)"

            for network in networks:
                ssid = network['SSID']
                bssid = network['BSSID']
                authentication = network.get('Authentication', 'N/A')
                signal = network.get('Signal', 'N/A')
                score = round(network.get('Score', 0))  # Round score to nearest integer
                wifi_hash = DatabaseManager.calculate_hash(ssid, bssid)

                data_to_insert = (ssid, bssid, authentication, signal, score, wifi_hash)
                cursor.execute(insert_query, data_to_insert)

            conn.commit()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return "Database error occurred."
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An unexpected error occurred."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return "Data sent to database successfully."
