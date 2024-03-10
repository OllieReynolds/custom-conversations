from PyQt5 import QtWidgets
import json
import os
from execution_pane import ExecutionPane
from info_pane import InfoPane

class TextTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TextTab, self).__init__(parent)
        self.parent = parent
        self.layout = QtWidgets.QHBoxLayout(self)

        self.pipelines_info = self.load_pipelines_info()
        self.execution_pane = ExecutionPane(self)
        self.layout.addWidget(self.execution_pane)

        self.info_pane = InfoPane(self)
        self.layout.addWidget(self.info_pane)

        self.setup_connections()

    def load_pipelines_info(self):
        pipelines_info_file = "pipelines_info.json"
        current_dir = os.path.dirname(__file__)
        full_path = os.path.join(current_dir, pipelines_info_file)

        with open(full_path, 'r') as file:
            pipelines_info = json.load(file)

        if not isinstance(pipelines_info, dict):
            raise ValueError("pipelines_info must be a dictionary")
        return pipelines_info

    def setup_connections(self):
        self.execution_pane.update_pipeline_options(list(self.pipelines_info.keys()))
        self.execution_pane.pipeline_options.currentTextChanged.connect(self.update_info_pane)
        self.update_info_pane()

    def update_info_pane(self):
        selected_pipeline = self.execution_pane.get_selected_pipeline()
        info = self.pipelines_info.get(selected_pipeline, {})
        self.info_pane.update_info(info)
