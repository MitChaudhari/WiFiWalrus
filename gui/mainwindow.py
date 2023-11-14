import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from gui.designer import Ui_MainWindow
from gui.network_scanner import NetworkScanner
from gui.database_manager import DatabaseManager

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scanner = NetworkScanner()
        self.db_manager = DatabaseManager()  # Initialize DatabaseManager
        self.ui.scanButton.clicked.connect(self.scanNetworks)

    def scanNetworks(self):
        self.ui.scanButton.setDisabled(True)
        self.ui.statusLabel.setText("Status: Scanning...")
        try:
            networks = self.scanner.scan()
            self.updateTable(networks)
            db_status = self.db_manager.send_to_database(networks)  # Send data to the database
            self.ui.statusLabel.setText(f"Status: {db_status}")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.ui.statusLabel.setText("Status: An error occurred while scanning.")
        finally:
            self.ui.scanButton.setDisabled(False)

    def updateTable(self, networks):
        self.ui.tableWidget.setRowCount(len(networks))
        for i, network in enumerate(networks):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(network['SSID']))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(network['BSSID']))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(network.get('Signal', 'N/A')))
            self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(network.get('Authentication', 'N/A')))
            self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(f"{network.get('Score', 0):.2f}"))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
