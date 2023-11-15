import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from gui.designer import Ui_MainWindow
from gui.network_scanner import NetworkScanner
from gui.database_manager import DatabaseManager
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import QTimer

class ScannerWorker(QThread):
    finished = pyqtSignal(list)  # Signal to emit the scanned networks
    
    def run(self):
        scanner = NetworkScanner()
        networks = scanner.scan()
        self.finished.emit(networks)  # Emit the results when done

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db_manager = DatabaseManager()  # Initialize DatabaseManager
        self.ui.scanButton.clicked.connect(self.scanNetworks)

        self.scanner_thread = ScannerWorker()  # Initialize the scanner thread
        self.scanner_thread.finished.connect(self.onScanComplete)  # Connect the finished signal
        
        # Initialize the progress dialog (not shown yet)
        self.progressDialog = QProgressDialog("Scanning networks...", None, 0, 0, self)
        self.progressDialog.setWindowTitle("Please Wait")
        self.progressDialog.setCancelButton(None)  # Disable cancel button
        self.progressDialog.setModal(True)
        self.progressDialog.setValue(0)
        
        # Initialize a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressDialog)
        self.elapsedTime = 0

    def scanNetworks(self):
        self.ui.scanButton.setDisabled(True)
        self.ui.statusLabel.setText("Status: Scanning...")
        self.showProgressDialog()  # Show the progress dialog
        self.scanner_thread.start()  # Start the scanner thread

    def showProgressDialog(self):
        self.elapsedTime = 0
        self.timer.start(1000)  # Update every second
        self.progressDialog.show()

    def updateProgressDialog(self):
        self.elapsedTime += 1
        self.progressDialog.setLabelText(f"Scanning networks... {self.elapsedTime} seconds elapsed")
    
    def onScanComplete(self, networks):
        self.updateTable(networks)
        db_status = self.db_manager.send_to_database(networks)
        self.ui.statusLabel.setText(f"Status: {db_status}")
        self.ui.scanButton.setDisabled(False)  # Re-enable the scan button

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
