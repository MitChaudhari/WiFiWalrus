import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QDialog, QVBoxLayout, QLabel, QPushButton,QHBoxLayout
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QPixmap, QBrush, QRadialGradient
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QPoint, QTimer, QPointF, QSize

from gui.designer import Ui_MainWindow
from gui.network_scanner import NetworkScanner
from gui.database_manager import DatabaseManager
class ScannerWorker(QThread):
    finished = pyqtSignal(list)  # Signal to emit the scanned networks
    def run(self):
        scanner = NetworkScanner()
        networks = scanner.scan()
        self.finished.emit(networks)  # Emit the results when done
        
class RecommendedNetworkDialog(QDialog):
    def __init__(self, network, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recommended Network")

        # Set up the layout
        layout = QVBoxLayout(self)

        # Add the body
        info_label = QLabel(f"""
            <p>We've scanned the available Wi-Fi networks and based on our analysis,
            the following network is recommended for you:</p>
            <p><b>Network Name (SSID):</b> {network.get('SSID', 'N/A')}<br>
            <b>Security Type:</b> {network.get('Authentication', 'N/A')}<br>
            <b>Signal Strength:</b> {network.get('Signal', 'N/A')}</p>
            <p>This network offers the best balance of security and signal strength,
            ensuring a more reliable and secure connection.</p>
        """)
        
        info_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF; /* White color for better visibility on gradient */
                font-size: 14px;
                margin: 10px;
            }
        """)
        
        layout.addWidget(info_label)

        # Add buttons
        connect_button = QPushButton("Connect")
        connect_button.setStyleSheet("""
            QPushButton {
                background-color: #5CDB95; /* Greenish color */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #379683; /* Darker green on hover */
            }
        """)
        connect_button.clicked.connect(self.on_connect)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #E27D60; /* Reddish color */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #C38D9E; /* Darker red on hover */
            }
        """)
        cancel_button.clicked.connect(self.reject)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(connect_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Set dialog properties
        self.setLayout(layout)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 15px;
            }
        """)

    def on_connect(self):
        # Placeholder for connection logic
        print("Connect to the network")
        self.accept()  # Closes the dialog
        
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor('#333333'))  # Dark grey
        gradient.setColorAt(1.0, QColor('#000000'))  # Black
        painter.fillRect(self.rect(), QBrush(gradient))

        super().paintEvent(event)  # Call the base class paint event

class MainWindow(QMainWindow):
    def __init__(self, navigation_manager):
        super(MainWindow, self).__init__()
        self.navigation_manager = navigation_manager
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db_manager = DatabaseManager()  # Initialize DatabaseManager
        self.setupSignals()

        self.scanner_thread = ScannerWorker()  # Initialize the scanner thread
        self.scanner_thread.finished.connect(self.onScanComplete)  # Connect the finished signal

        self._gradient_colors = [
            QColor('#0E0A1B'),  # Blue-Magenta
            QColor('#5333EC'),  # Dark Purple
            QColor('#FF4500'),  # Dark Orange
        ]
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(10)  # Adjust the timer interval for slower animation

        self._animation_step = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPointF(self.width() / 2, self.height() / 2)
        max_radius = max(self.width(), self.height()) / 2
        gradient = QRadialGradient(center, max_radius)

        # Gradual color stops for smooth transition
        for i, color in enumerate(self._gradient_colors):
            pos = i / (len(self._gradient_colors) - 1)
            gradient.setColorAt(pos, color)

        # Subtle animation in the most inner circle
        inner_color = QColor('#FF4500')  # Dark Orange
        inner_color.setAlpha(int(150 + 105 * math.sin(self._animation_step / 50)))
        gradient.setColorAt(0.1, inner_color)  # Adjust the position for size of the animated circle

        # The outermost color should be black
        gradient.setColorAt(1, QColor('black'))

        painter.fillRect(self.rect(), gradient)
        painter.end()

        # Increment the step for the next frame
        self._animation_step += 1

    def sizeHint(self):
        return QSize(1200, 800)  # Preferred size of the widget

    def setupSignals(self):
        # Setup signals for UI components
        self.ui.scanButton.clicked.connect(self.scanNetworks)
        self.ui.homeButton.clicked.connect(self.navigation_manager.show_home)
        self.ui.aboutButton.clicked.connect(self.navigation_manager.show_about_us)
        self.ui.getStartedButton.clicked.connect(self.navigation_manager.show_get_started)

    def scanNetworks(self):
        self.ui.scanButton.setText("Scanning...")  # Set the button text to indicate scanning
        self.ui.scanButton.setDisabled(True)  # Disable the button to prevent multiple clicks
        self.scanner_thread.start()  # Start the scanner thread

    def onScanComplete(self, networks):
        self.updateTable(networks)
        db_status = self.db_manager.send_to_api(networks)
        self.ui.scanButton.setText("Scan")  # Reset the button text back to "Scan"
        self.ui.scanButton.setEnabled(True)  # Re-enable the button
        self.showRecommendation(networks)  # Show the recommendation dialog

    def updateTable(self, networks):
        num_of_networks = len(networks)
        row_height = 30  # Assuming each row is approximately 30 pixels high
        header_height = 30  # A header, its height

        # Set the number of rows in the table
        self.ui.tableWidget.setRowCount(num_of_networks)
        
        # Calculate the total height the table needs to be to fit all rows and header
        table_height = (row_height * (num_of_networks + 1)) + header_height
        
        # Set the table's dimensions - adjust as needed
        self.ui.tableWidget.setMinimumHeight(table_height)
        self.ui.tableWidget.setMaximumHeight(table_height)

        # Now, populate the table with the data
        for i, network in enumerate(networks):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(network.get('SSID', 'N/A')))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(network.get('BSSID', 'N/A')))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(network.get('Signal', 'N/A')))
            self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(network.get('Authentication', 'N/A')))
            self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(f"{network.get('Score', 0):.2f}"))
            
        self.ui.centralwidget.layout().update()
        
    def showRecommendation(self, networks):
        if networks:
            recommended_network = networks[0]  # Assuming the first network is the recommended one
            self.recommendation_dialog = RecommendedNetworkDialog(recommended_network, self)
            self.recommendation_dialog.exec_()  # Show the dialog

def main():
    app = QApplication(sys.argv)
    navigation_manager = None  # Initialize or import your navigation manager here
    window = MainWindow(navigation_manager)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

