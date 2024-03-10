from PyQt5 import QtWidgets

class InfoPane(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(InfoPane, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.info_text_area = QtWidgets.QPlainTextEdit(self)
        self.info_text_area.setReadOnly(True)
        self.layout.addWidget(self.info_text_area)

    def update_info(self, info):
        info_text = f"Description: {info.get('description', 'No description available')}\n\n" \
                    f"Usage: {info.get('usage', 'No usage information available')}\n\n" \
                    f"Sample Input: {info.get('sample_input', 'No sample input available')}\n\n" \
                    f"Expected Output: {info.get('expected_output', 'No expected output available')}"
        self.info_text_area.setPlainText(info_text)
