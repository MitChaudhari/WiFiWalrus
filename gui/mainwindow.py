import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from gui.designer import Ui_MainWindow
from gui.network_scanner import NetworkScanner
from gui.database_manager import DatabaseManager
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QProgressDialog, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QProgressDialog
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt  # Make sure Qt is included here
from PyQt5.QtWidgets import QDialog, QVBoxLayout

class LoadingDialog(QDialog):
    def __init__(self, gif_path, parent=None):
        super(LoadingDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Loading...")

        # Create a label to hold the GIF
        self.gifLabel = QLabel()
        movie = QMovie(gif_path)
        self.gifLabel.setMovie(movie)
        movie.start()

        # Create a label for the text
        self.textLabel = QLabel("Scanning the airwaves...")
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setStyleSheet("color: white;")

        # Set the dialog layout
        layout = QVBoxLayout()
        layout.addWidget(self.gifLabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.textLabel)
        self.setLayout(layout)

        # Set the dialog's stylesheet
        self.setStyleSheet("QDialog { background-color: black; }")

        # Adjust the size of the QDialog to fit the content
        self.adjustSize()

    def update_text(self, text):
        self.textLabel.setText(text)



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
        self.progressDialog.setAutoClose(False)
        
        # Initialize a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressDialog)
        self.elapsedTime = 0
        
        gifPath = os.path.abspath("../assets/gif1.gif")  # Make sure this path is correct
        self.loadingDialog = LoadingDialog(gifPath, self)

    def scanNetworks(self):
        self.ui.scanButton.setDisabled(True)
        self.ui.statusLabel.setText("Status: Scanning...")
        self.loadingDialog.show()  # Show the loading dialog
        self.timer.start(1000)  # Start the timer to update the text
        self.scanner_thread.start()  # Start the scanner thread

    def updateProgressDialog(self):
        phrases = ["Scanning the airwaves...", "Almost there...", "Hang tight, we're scanning...", "Just a moment..."]
        current_phrase = phrases[self.elapsedTime % len(phrases)]
        self.loadingDialog.update_text(current_phrase)  # Update the text in the loading dialog
        self.elapsedTime += 1
    
    def onScanComplete(self, networks):
        self.updateTable(networks)
        db_status = self.db_manager.send_to_database(networks)
        self.ui.statusLabel.setText(f"Status: {db_status}")
        self.loadingDialog.accept()  # Close the loading dialog
        self.timer.stop()  # Stop the timer
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
