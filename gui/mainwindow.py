# mainwindow.py

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

    def scanNetworks(self):  # This method should be inside the MainWindow class
        try:
            self.ui.statusLabel.setText("Status: Scanning...")
            networks = self.scanner.scan()  # This should retrieve the list of networks

            print(networks)  # Debugging purpose

            self.updateTable(networks)  # Update the table with the new data
        except Exception as e:
            print(f"An error occurred: {e}")  # This line will help catch any errors
            self.ui.statusLabel.setText("Status: An error occurred while scanning.")

    def updateTable(self, networks):  # This method should also be inside the MainWindow class
        self.ui.tableWidget.setRowCount(len(networks))

        for i, network in enumerate(networks):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(network['SSID']))
            # Make sure your table has enough columns to set these items.
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(network['BSSID']))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(network['Security']))

# The rest of your main function remains unchanged.

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
