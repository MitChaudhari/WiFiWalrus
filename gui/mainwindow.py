import sys
import hashlib
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from gui.designer import Ui_MainWindow
from gui.network_scanner import NetworkScanner

# Database connection parameters
db_config = {
    'user': 'root',
    'password': 'ipro497db',
    'host': 'ec2-3-12-150-224.us-east-2.compute.amazonaws.com',
    'database': 'ipro1'
}

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scanner = NetworkScanner()
        self.ui.scanButton.clicked.connect(self.scanNetworks)

    def calculate_hash(self, ssid, bssid):
        data = f"{ssid}{bssid}".encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def scanNetworks(self):
        # Disable the button to prevent multiple scans at the same time
        self.ui.scanButton.setDisabled(True)
        self.ui.statusLabel.setText("Status: Scanning...")
        try:
            networks = self.scanner.scan()
            self.updateTable(networks)
            self.sendToDatabase(networks)
            self.ui.statusLabel.setText("Status: Scan complete.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.ui.statusLabel.setText("Status: An error occurred while scanning.")
        finally:
            # Re-enable the scan button after the scan is complete or if an error occurs
            self.ui.scanButton.setDisabled(False)


    def updateTable(self, networks):
        self.ui.tableWidget.setRowCount(len(networks))
        for i, network in enumerate(networks):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(network['SSID']))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(network['BSSID']))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(network.get('Signal', 'N/A')))
            self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(network.get('Authentication', 'N/A')))
            self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(str(network.get('Score', 0))))

    def sendToDatabase(self, networks):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            insert_query = "INSERT INTO connections (SSID, BSSID, Authentication, Signal, Score, SHA256_Hash) VALUES (%s, %s, %s, %s, %s, %s)"

            for network in networks:
                ssid = network['SSID']
                bssid = network['BSSID']
                authentication = network.get('Authentication', 'N/A')
                signal = network.get('Signal', 'N/A')
                score = network.get('Score', 0)
                wifi_hash = self.calculate_hash(ssid, bssid)

                data_to_insert = (ssid, bssid, authentication, signal, score, wifi_hash)
                cursor.execute(insert_query, data_to_insert)

            conn.commit()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            self.ui.statusLabel.setText("Status: Database error occurred.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.ui.statusLabel.setText("Status: An unexpected error occurred.")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()