# gui/navigation_manager.py
class NavigationManager:
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget
        self.pages = {
            'home': None,
            'about_us': None,
            'get_started': None
        }

    def show_home(self):
        if not self.pages['home']:
            from .home_page import HomePage
            self.pages['home'] = HomePage(self)
            self.stacked_widget.addWidget(self.pages['home'])
        self.stacked_widget.setCurrentWidget(self.pages['home'])

    def show_about_us(self):
        if not self.pages['about_us']:
            from .about_us import AboutUs
            self.pages['about_us'] = AboutUs(self)
            self.stacked_widget.addWidget(self.pages['about_us'])
        self.stacked_widget.setCurrentWidget(self.pages['about_us'])

    def show_get_started(self):
        if not self.pages['get_started']:
            from .mainwindow import MainWindow
            self.pages['get_started'] = MainWindow(self)
            self.stacked_widget.addWidget(self.pages['get_started'])
        self.stacked_widget.setCurrentWidget(self.pages['get_started'])

