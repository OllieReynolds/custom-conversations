from PyQt5 import QtWidgets
from theme_selector import ThemeSelector
from text_tab import TextTab

class TransformersGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TransformersGUI, self).__init__(parent)
        self.setWindowTitle("Hugging Face Transformers GUI")

        self.initUI()
        self.theme_selector = ThemeSelector(self)

    def initUI(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        tab_widget = QtWidgets.QTabWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.addWidget(tab_widget)

        text_tab = TextTab(self)
        tab_widget.addTab(text_tab, "Text")

        image_tab = QtWidgets.QWidget()
        tab_widget.addTab(image_tab, "Image Generation")
        
        video_tab = QtWidgets.QWidget()
        tab_widget.addTab(video_tab, "Video Generation")
        
        audio_tab = QtWidgets.QWidget()
        tab_widget.addTab(audio_tab, "Audio Generation")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = TransformersGUI()
    mainWin.show()
    sys.exit(app.exec_())
