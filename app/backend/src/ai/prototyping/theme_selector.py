from PyQt5 import QtWidgets, QtCore
import os

class ThemeSelector:
    def __init__(self, window):
        self.window = window
        self.init_theme_menu()

    def init_theme_menu(self):
        menubar = self.window.menuBar()
        viewMenu = menubar.addMenu('View')
        themeMenu = viewMenu.addMenu('Theme')

        self.themeActionGroup = QtWidgets.QActionGroup(self.window)

        self.loadExternalThemes(themeMenu)

        currentStyle = QtWidgets.QApplication.style().objectName().lower()
        for action in self.themeActionGroup.actions():
            if action.data().lower() == currentStyle:
                action.setChecked(True)

    def addStyleAction(self, menu, styleName):
        styleAction = QtWidgets.QAction(styleName.capitalize(), self.window, checkable=True)
        styleAction.setData(styleName.lower())
        self.themeActionGroup.addAction(styleAction)
        menu.addAction(styleAction)
        styleAction.triggered.connect(lambda checked, action=styleAction: self.changeStyle(checked, action))

    def changeStyle(self, checked, action):
            if checked:
                QtWidgets.qApp.setStyleSheet("")
                self.applyExternalStyle(action.data())

    def applyExternalStyle(self, styleName):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for ext in ['.qss', '.css']:
            stylesheet_path = os.path.join(current_dir, 'themes', f'{styleName}{ext}')
            if os.path.exists(stylesheet_path):
                with open(stylesheet_path, 'r') as file:
                    self.window.setStyleSheet(file.read())
                break

    def loadExternalThemes(self, menu):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(current_dir, 'themes')

        if not os.path.exists(themes_dir):
            os.makedirs(themes_dir)

        for filename in os.listdir(themes_dir):
            if filename.endswith(('.qss', '.css')):
                styleName = filename.rsplit('.', 1)[0]
                self.addStyleAction(menu, styleName)
