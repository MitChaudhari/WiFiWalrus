import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt5.QtGui import QPixmap, QMovie, QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QPoint


class HomePage(QWidget):
    def __init__(self, navigation_manager):
        super().__init__()
        self.navigation_manager = navigation_manager
        self.initUI()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))

        # Start with black
        gradient.setColorAt(0, QColor('black'))
        # Start blending into dark purple (#010314)
        gradient.setColorAt(0.75, QColor('#010314'))
        # Transition into bright purple (#592DD1)
        gradient.setColorAt(0.90, QColor('#592DD1'))
        # End with white (#FFFFFF)
        gradient.setColorAt(1, QColor('#FFFFFF'))

        painter.fillRect(self.rect(), gradient)
        painter.end()

    def initUI(self):
        self.setWindowTitle('WiFiWalrus - Home')
        self.setGeometry(300, 300, 1200, 800)
        # Set only the color and font style, not the background
        self.setStyleSheet("""
            QWidget {
                color: white;
                font-family: 'Helvetica', sans-serif;
            }
        """)
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 20, 50, 20)

        # Top layout for logo, app name, and navigation
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Logo
        logo = QLabel(self)
        logo_pixmap = QPixmap('assets/logo.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(logo_pixmap)
        top_layout.addWidget(logo)

        # App name
        app_name = QLabel('WiFiWalrus', self)
        app_name.setStyleSheet("font-size: 30px;")
        top_layout.addWidget(app_name)
        top_layout.addStretch()

        # Navigation buttons
        home_button = QPushButton('Home', self)
        about_button = QPushButton('About Us', self)
        get_started_button = QPushButton('Get Started', self)

        # Connect buttons to navigation manager's methods
        home_button.clicked.connect(self.navigation_manager.show_home)
        about_button.clicked.connect(self.navigation_manager.show_about_us)
        get_started_button.clicked.connect(self.navigation_manager.show_get_started)

        # Apply styles to the buttons
        button_styles = """
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
                background-color: #2c2c2c;  /* Dark grey background on hover */
            }
        """
        home_button.setStyleSheet(button_styles)
        about_button.setStyleSheet(button_styles)
        get_started_button.setStyleSheet(button_styles)

        # Add buttons to the top layout
        top_layout.addWidget(home_button)
        top_layout.addWidget(about_button)
        top_layout.addWidget(get_started_button)
        main_layout.addLayout(top_layout)

        # Main content layout
        content_layout = QHBoxLayout()

        # Left content layout
        left_content_layout = QVBoxLayout()
        left_content_layout.addStretch(1)  # Add stretch to push content down

        # Phrase label
        phrase_label = QLabel("Seamless Scanning, Robust Security –Your Wi-Fi Connectivity, Elevated.", self)
        phrase_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        phrase_label.setWordWrap(True)
        phrase_label.setFixedWidth(600)  # Adjust the fixed width as needed
        left_content_layout.addWidget(phrase_label)

        # Description label
        desc_label = QLabel("WiFiWalrus is your digital scout, leading you to safe and strong Wi-Fi networks with ease. Experience seamless connectivity and confident browsing, anywhere, anytime.", self)
        desc_label.setStyleSheet("font-size: 18px;")
        desc_label.setWordWrap(True)
        desc_label.setFixedWidth(600)  # Adjust the fixed width as needed
        left_content_layout.addWidget(desc_label)

        # Get Started button
        get_started_main_button = QPushButton("Get Started", self)
        get_started_main_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: black;  /* Text color */
                background-color: white;  /* Background color */
                border: 2px solid white;
                border-radius: 20px;
                padding: 10px 20px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #a6a6a6;  /* Medium grey background on hover */
            }
        """)
        get_started_main_button.setFixedWidth(150)  # Set a fixed width for the button
        get_started_main_button.clicked.connect(self.show_main_window)
        left_content_layout.addWidget(get_started_main_button)

        left_content_layout.addStretch(1)  # Add stretch to push content up, centering it vertically
        content_layout.addLayout(left_content_layout, 2)  # Adjust the stretch factor to give more space

        # Right content layout with GIF
        right_content_layout = QVBoxLayout()
        right_content_layout.addStretch(1)  # Add stretch to align GIF vertically

        gif_label = QLabel(self)
        gif_movie = QMovie('assets/wifiBar.gif')
        gif_label.setMovie(gif_movie)
        gif_movie.start()
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setFixedSize(600, 300)
        right_content_layout.addWidget(gif_label)

        right_content_layout.addStretch(1)
        content_layout.addLayout(right_content_layout, 1)  # Adjust the stretch factor if needed

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def show_about_us(self):
        self.navigation_manager.show_about_us()

    def show_main_window(self):
        self.navigation_manager.show_get_started()

    def show_home(self):
        self.show()

# The block for standalone testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Create a mock navigation manager or pass the real one
    mock_navigation_manager = None
    home_page = HomePage(mock_navigation_manager)
    home_page.show()
    sys.exit(app.exec_())