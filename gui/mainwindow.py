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
        
    # Inside your MainWindow class in mainwindow.py

def scanNetworks(self):
    try:
        self.ui.statusLabel.setText("Status: Scanning...")
        networks = self.scanner.scan()  # This should retrieve the list of networks

        # You can print 'networks' here to verify that it contains the expected data
        print(networks)

        self.updateTable(networks)
    except Exception as e:
        print(f"An error occurred: {e}")  # This line will help catch any errors
        self.ui.statusLabel.setText("Status: An error occurred while scanning.")

# ...

def updateTable(self, networks):
    self.ui.tableWidget.setRowCount(len(networks))

    for i, network in enumerate(networks):
        self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(network['SSID']))
        self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(network['BSSID']))
        self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(network['Security']))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
