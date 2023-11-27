from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMainWindow, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        
        # Central Widget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main Layout
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(50, 20, 50, 20)

        # Header Layout
        self.headerLayout = QHBoxLayout()

        # Logo
        self.logo = QLabel(self.centralwidget)
        self.logo.setPixmap(QPixmap('assets/logo.png').scaled(100, 100, Qt.KeepAspectRatio))
        self.headerLayout.addWidget(self.logo)

        # App Name
        self.appName = QLabel("WiFiWalrus", self.centralwidget)
        self.appName.setFont(QFont("Helvetica", 30))
        self.appName.setStyleSheet("color: white;")
        self.headerLayout.addWidget(self.appName)

        # Stretch to push the navigation to the right
        self.headerLayout.addStretch(1)

        # Navigation Buttons
        nav_button_style = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: transparent;
                border: 1px solid white;
                border-radius: 15px;
                padding: 10px 20px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """
        self.homeButton = QPushButton("Home", self.centralwidget)
        self.aboutButton = QPushButton("About Us", self.centralwidget)
        self.getStartedButton = QPushButton("Get Started", self.centralwidget)
        self.homeButton.setStyleSheet(nav_button_style)
        self.aboutButton.setStyleSheet(nav_button_style)
        self.getStartedButton.setStyleSheet(nav_button_style)

        # Add navigation buttons to the header layout
        self.headerLayout.addWidget(self.homeButton)
        self.headerLayout.addWidget(self.aboutButton)
        self.headerLayout.addWidget(self.getStartedButton)

        # Add header layout to the main layout
        self.mainLayout.addLayout(self.headerLayout)

        # Title Label for the Network Scanner
        self.titleLabel = QLabel("Network Scanner", self.centralwidget)
        self.titleLabel.setFont(QFont("Helvetica", 30))  # Increased font size for visibility
        self.titleLabel.setStyleSheet("color: white; margin-bottom: 20px;")  # Add margin at the bottom
        self.mainLayout.addWidget(self.titleLabel, alignment=Qt.AlignCenter)  # Center alignment
        
        #Use a spacer item to push the table down a bit
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem)  # Add spacer item before the table

        table_widget_style = """
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 20px;  /* Rounded corners */
            }
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.5);
                padding: 10px;
                border: none;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }
            QTableWidgetItem {
                padding: 10px;
            }
            """
        # Initialize the table widget with fixed dimensions
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["SSID", "BSSID", "Signal", "Security", "Score"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Adjust column sizes automatically
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setStyleSheet(table_widget_style)
        self.tableWidget.setRowCount(10)  # Set the number of rows to 10

        # Assuming each row is 30 pixels high, including the header, set a fixed height
        row_height = 30
        header_height = 30
        total_height = (row_height * 10) + header_height
        self.tableWidget.setFixedSize(600, total_height)  # Width is 600, height is calculated

        # Place the table within a layout to center it in the available space
        tableLayout = QVBoxLayout()
        tableLayout.addStretch(10)  # Add stretch to center the table vertically
        tableLayout.addWidget(self.tableWidget, 0, Qt.AlignCenter)  # Center horizontally and vertically
        tableLayout.addStretch()  # Add stretch to center the table vertically
        self.mainLayout.addLayout(tableLayout)
    
        # Define the stylesheet for the scan button
        scan_button_style = """
            QPushButton {
                font-size: 18px;  /* Increased font size */
                font-weight: bold;
                color: white;
                background-color: #5333EC;  /* New gradient theme color */
                border-radius: 8px;
                padding: 15px 30px;  /* Increased padding for a larger button */
                margin-top: 25px;
            }
            QPushButton:disabled {
                background-color: #7F6AC7;  /* A lighter purple color to indicate scanning */
                color: #E0E0E0;  /* A light grey color for text */
            }
        """
        
        # Scan Button
        self.scanButton = QPushButton("Scan", self.centralwidget)
        self.scanButton.setFont(QFont("Helvetica", 18))
        self.scanButton.setStyleSheet(scan_button_style)
        self.scanButton.setFixedSize(200, 75)  # Set a fixed size for the button
        self.mainLayout.addWidget(self.scanButton, alignment=Qt.AlignCenter)  # Center alignment

        # Center the button
        buttonBox = QHBoxLayout()
        buttonBox.addStretch(1)
        buttonBox.addWidget(self.scanButton)
        buttonBox.addStretch(1)
        self.mainLayout.addLayout(buttonBox)

        # Set the main layout to the central widget
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("WiFiWalrus - Network Scanner")

        # This ensures all widgets are centered in the QVBoxLayout
        self.mainLayout.addStretch(1)


