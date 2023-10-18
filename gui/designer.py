# designer.py

from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTableWidget, QWidget

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Central Widget
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Vertical Layout to hold all widgets
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # Table to display Networks
        self.tableWidget = QTableWidget(self.centralwidget)
        
        # Set the number of columns you need; for example, 3 for SSID, BSSID, and Security
        # Add more if you have other details to show
        self.tableWidget.setColumnCount(3)  
        
        # Set the header labels based on the information you're showing
        self.tableWidget.setHorizontalHeaderLabels(['SSID', 'BSSID', 'Security']) 
        
        self.verticalLayout.addWidget(self.tableWidget)

        # Scan Button
        self.scanButton = QPushButton("Scan", self.centralwidget)
        self.verticalLayout.addWidget(self.scanButton)

        # Status Label
        self.statusLabel = QLabel("Status: Idle", self.centralwidget)
        self.verticalLayout.addWidget(self.statusLabel)

        # Main Window Configuration
        MainWindow.setWindowTitle("Network Scanner")

        # You might want to add resizing options or other property changes to better accommodate the new layout.
