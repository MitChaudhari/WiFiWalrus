import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.home_page import HomePage
from gui.navigation_manager import NavigationManager

class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.navigation_manager = NavigationManager(self.stacked_widget)
        self.initUI()

    def initUI(self):
        # Show the initial page (e.g., HomePage)
        home_page = HomePage(self.navigation_manager)
        self.stacked_widget.addWidget(home_page)
        self.stacked_widget.setCurrentWidget(home_page)

def main():
    app = QApplication(sys.argv)
    main_window = MainApplicationWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
