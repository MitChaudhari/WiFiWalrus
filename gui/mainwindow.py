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
        try:
            self.ui.statusLabel.setText("Status: Scanning...")
            networks = self.scanner.scan()
            print(networks)
            self.updateTable(networks)
            self.sendToDatabase(networks)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.ui.statusLabel.setText("Status: An error occurred while scanning.")

    def updateTable(self, networks):
        self.ui.tableWidget.setRowCount(len(networks))
        for i, network in enumerate(networks):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(network['SSID']))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(network['BSSID']))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(network.get('Signal', 'N/A')))
            self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(network.get('Security', 'N/A')))
            self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(network.get('Authentication', 'N/A')))

    def sendToDatabase(self, networks):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO connections (SSID, BSSID, Security, Signal, Authentication, Score, SHA256_Hash) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        for network in networks:
            ssid = network['SSID']
            bssid = network['BSSID']
            security = network.get('Security', 'N/A')
            signal = network.get('Signal', 'N/A')
            authentication = network.get('Authentication', 'N/A')
            score = network.get('Score', 0)
            wifi_hash = self.calculate_hash(ssid, bssid)

            data_to_insert = (ssid, bssid, security, signal, authentication, score, wifi_hash)
            cursor.execute(insert_query, data_to_insert)

        conn.commit()
        cursor.close()
        conn.close()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
