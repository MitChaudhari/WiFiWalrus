from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QStatusBar, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Network Scanner")
        
        # Top Bar
        self.scan_button = QPushButton('Scan')
        self.scan_label = QLabel('Press Scan to start')
        
        # Main Section
        self.network_list = QTableWidget()
        self.network_list.setColumnCount(5)
        self.network_list.setHorizontalHeaderLabels(['SSID', 'Security Type', 'Status', 'Score', 'Info'])
        
        # Status Bar
        self.status_bar = QStatusBar()
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.scan_button)
        layout.addWidget(self.scan_label)
        layout.addWidget(self.network_list)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)
        self.setStatusBar(self.status_bar)

    def update_network_list(self, networks):
        self.network_list.setRowCount(len(networks))
        for i, network in enumerate(networks):
            self.network_list.setItem(i, 0, QTableWidgetItem(network['ssid']))
            # ... similarly add items for other columns
