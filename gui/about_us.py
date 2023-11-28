import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,QSizePolicy
from PyQt5.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPoint

class AboutUs(QWidget):
    def __init__(self, navigation_manager):
        super().__init__()
        self.navigation_manager = navigation_manager
        self.initUI()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        gradient.setColorAt(0, QColor('black'))
        gradient.setColorAt(0.5, QColor('#ad5389'))
        gradient.setColorAt(1, QColor('#ffecd2'))

        painter.fillRect(self.rect(), gradient)
        painter.end()

    def initUI(self):
        self.setWindowTitle('About Us - WiFiWalrus')
        self.setGeometry(300, 300, 1200, 800)

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
        app_name.setStyleSheet("font-size: 30px; color: white;")
        top_layout.addWidget(app_name)
        top_layout.addStretch()

        # Navigation buttons
        home_button = QPushButton('Home', self)
        about_button = QPushButton('About Us', self)
        get_started_button = QPushButton('Get Started', self)

        # Connect buttons to their functions
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

        top_layout.addWidget(home_button)
        top_layout.addWidget(about_button)
        top_layout.addWidget(get_started_button)

        main_layout.addLayout(top_layout)

        # Content layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)  # Adjust spacing if necessary

        # Title "About Us" in cursive
        title_label = QLabel('About Us', self)
        title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: white; font-family: 'Brush Script MT', cursive;")
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)

        # About Us content in a rounded box within a QHBoxLayout to center it
        about_content_layout = QHBoxLayout()
        about_content_layout.addStretch()  # Add stretch to center the label
        
        # Now we set this font to the QLabel
        font = QFont("Verdana", 16)
        about_content = QLabel()
        about_content.setFont(font)
        about_content.setTextFormat(Qt.RichText)  # Set text format to Rich Text
        about_content.setText("""
            <p><strong>Where It All Began</strong><br>
            In an era where digital connectivity is as essential as the air we breathe, Wi-Fi Walrus emerged as a beacon of secure connection. Our goal was simple: help people find safe Wi-Fi networks easily.</p>

            <p><strong>What We've Made</strong><br>
            Our little creation scans for Wi-Fi networks and gives you the info you need to pick a safe one. It's like having a smart friend who knows a bit about online safety.</p>

            <p><strong>Who We Are</strong><br>
            We're a bunch of students from different areas—some of us code, some design, and others write up all the info. We all pitched in to build Wi-Fi Walrus.</p>

            <p><strong>Our App's Journey</strong><br>
            It's still early days for our app. We see it as a starting point, and we're excited about how much better it can get with a little more time and work.</p>

            <p><strong>Be Part of Our Story</strong><br>
            We'd love for you to try Wi-Fi Walrus and share your thoughts. Your feedback is super valuable, and who knows? Your suggestion might be what makes our project awesome. Here's to safer browsing, together.</p>
        """)
        about_content.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        about_content.setWordWrap(True)
        about_content.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Center-align the text within the label

        # Set the size policy to scale with the window
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        about_content.setSizePolicy(size_policy)
        about_content.setMaximumWidth(700)  # Adjust the maximum width as needed
        about_content.setMinimumWidth(400)  # Ensure a minimum width for readability

        about_content_layout.addWidget(about_content)
        about_content_layout.addStretch()  # Add stretch to center the label

        content_layout.addLayout(about_content_layout)
        
        lets_get_started_button = QPushButton("Let's Get Started", self)
        lets_get_started_button.clicked.connect(self.show_get_started)
        lets_get_started_button.setStyleSheet("""
            QPushButton {
                font-size: 25px;  /* Increased font size */
                font-weight: bold;
                color: white;
                background-color: #ad5389;  /* Button background color */
                border-radius: 20px;  /* Rounded corners */
                padding: 20px 45px;  /* Increased padding for more height */
                margin-top: 20px;  /* Space above the button */
            }
            QPushButton:hover {
                background-color: #ffecd2;  /* Button hover color */
                color: black;
            }
        """)

        # Adjust size policy and maximum width to make the button responsive
        lets_get_started_button.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        lets_get_started_button.setMaximumWidth(300)  # Adjust the maximum width as needed

        lets_get_started_button_layout = QHBoxLayout()
        lets_get_started_button_layout.addStretch()
        lets_get_started_button_layout.addWidget(lets_get_started_button)
        lets_get_started_button_layout.addStretch()

        content_layout.addLayout(lets_get_started_button_layout)

        # Adjust this stretch to move content upward
        content_layout.addStretch(1)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def show_home(self):
        self.navigation_manager.show_home()

    def show_about_us(self):
        self.show()

    def show_get_started(self):
        self.navigation_manager.show_get_started()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    about_us_page = AboutUs()
    about_us_page.show()
    sys.exit(app.exec_())
