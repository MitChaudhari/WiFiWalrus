#Contains the hand-coded design of the UI components.
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
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['SSID', 'Security', 'Score', 'Recommendation', 'Detail'])
        self.verticalLayout.addWidget(self.tableWidget)

        # Scan Button
        self.scanButton = QPushButton("Scan", self.centralwidget)
        self.verticalLayout.addWidget(self.scanButton)

        # Status Label
        self.statusLabel = QLabel("Status: Idle", self.centralwidget)
        self.verticalLayout.addWidget(self.statusLabel)

        # Main Window Configuration
        MainWindow.setWindowTitle("Network Scanner")