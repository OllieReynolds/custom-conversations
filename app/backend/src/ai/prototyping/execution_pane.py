# execution_pane.py

from PyQt5 import QtWidgets
from transformers import pipeline

class ExecutionPane(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(ExecutionPane, self).__init__(parent)
        self.initUI()
        self.pipeline_functions = self.initialize_pipeline_functions()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.pipeline_options = QtWidgets.QComboBox(self)
        layout.addWidget(self.pipeline_options)

        self.input_text_area = QtWidgets.QPlainTextEdit(self)
        layout.addWidget(self.input_text_area)

        execute_button = QtWidgets.QPushButton("Execute", self)
        execute_button.clicked.connect(self.on_execute)
        layout.addWidget(execute_button)

        self.result_text_area = QtWidgets.QPlainTextEdit(self)
        self.result_text_area.setReadOnly(True)
        layout.addWidget(self.result_text_area)

    def initialize_pipeline_functions(self):
        return {
            'Feature Extraction': lambda text: pipeline("feature-extraction")(text)[0][0][:5],
            'Fill-Mask': lambda text: pipeline("fill-mask")(text),
            'NER': lambda text: pipeline("ner")(text),
            'Question Answering': lambda text: pipeline("question-answering")(question=text.split('.', 1)[0], context=text.split('.', 1)[1]) if '.' in text else "Invalid input format for QA.",
            'Sentiment Analysis': lambda text: pipeline("sentiment-analysis")(text),
            'Summarization': lambda text: pipeline("summarization")(text),
            'Text Generation': lambda text: pipeline("text-generation")(text, max_length=50),
            'Translation (EN to FR)': lambda text: pipeline("translation_en_to_fr")(text),
            'Zero-Shot Classification': lambda text: pipeline("zero-shot-classification")(text, candidate_labels=['education', 'politics', 'business']),
        }
        
    def on_execute(self):
        selected_pipeline = self.get_selected_pipeline()
        input_text = self.get_input_text()
        function = self.pipeline_functions.get(selected_pipeline, lambda text: "Unsupported pipeline")
        result = function(input_text)
        self.set_result_text(str(result))

    def update_pipeline_options(self, options):
        self.pipeline_options.clear()
        self.pipeline_options.addItems(options)

    def get_selected_pipeline(self):
        return self.pipeline_options.currentText()

    def get_input_text(self):
        return self.input_text_area.toPlainText().strip()

    def set_result_text(self, text):
        self.result_text_area.setPlainText(text)
