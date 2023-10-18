import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from gui.designer import Ui_MainWindow
from gui.network_scanner import NetworkScanner

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Setup Network Scanner
        self.scanner = NetworkScanner()
        
        # Connect the Scan button to the scanNetworks method
        self.ui.scanButton.clicked.connect(self.scanNetworks)
        
    def scanNetworks(self):
        try:
            self.ui.statusLabel.setText("Status: Scanning...")
            networks = self.scanner.scan()
            print(networks)  # Debugging line to understand the structure of returned data
            self.updateTable(networks)  # Update the table with the results received from network_scanner.py
            self.ui.statusLabel.setText("Status: Idle")
        except Exception as e:
            self.ui.statusLabel.setText(f"Error: {str(e)}")
        
    def updateTable(self, networks):
        self.ui.tableWidget.setRowCount(len(networks))
        for i, network in enumerate(networks):
            # Extracting information from the network dictionary
            ssid = network.get('SSID', '')
            bssid = network.get('BSSID', '')  # Include this if it's in your dictionary
            security = ' / '.join(network.get('Security', []))  # Joining the list into a string

            # Adding items to the table
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(ssid))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(bssid))  # Adjust column index if different
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(security))  # Adjust column index if different
            # Add more fields as necessary, adjusting the column index each time
            
            # If you have additional data to add to the table, continue the pattern above.

    def getNetworksFromBackend(self):
        # This method should interact with the backend to get the list of networks.
        # Placeholder for now.
        return []

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
