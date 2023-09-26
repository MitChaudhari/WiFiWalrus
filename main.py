import sys
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)  # Creating an instance of QApplication
    
    window = MainWindow()  # Creating an instance of your MainWindow class
    window.show()  # Showing the main window
    
    sys.exit(app.exec_())  # Starting the application event loop

if __name__ == "__main__":
    main()  # Calling main function when the script is executed
