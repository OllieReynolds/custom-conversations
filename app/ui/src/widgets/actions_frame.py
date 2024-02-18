import threading
import tkinter as tk

import requests
from app.ui.src.components.action_panel_stylised_title import ActionPanelStylizedTitle

from app.ui.src.components.stylised_title import StylizedTitle

class ActionFrame(tk.Frame):
    def __init__(self, parent, textColor, backendURL, checkCUDACallback, updateStatusCallback, drawGeneratedConversationCallback, font=None, *args, **kwargs):
        super().__init__(parent, bg='#333333', *args, **kwargs)
        self.textColor = textColor
        self.backendURL = backendURL
        self.checkCUDACallback = checkCUDACallback
        self.updateStatusCallback = updateStatusCallback
        self.drawGeneratedConversationCallback = drawGeneratedConversationCallback
        self.font = font
        self._createWidgets()

    def _createWidgets(self):
        title = StylizedTitle(self, "Action Panel", textColor=self.textColor, bgColor='#333333')
        title.pack(fill=tk.X)

        model_operations = {
            "Retrain Model": self._placeholderAction,
            "Stop Training": self._placeholderAction,
            "Evaluate Model": self._placeholderAction,
            "Download Model": self._placeholderAction,
            "Save Current State": self._placeholderAction,
            "Load State": self._placeholderAction,
            "Update Model": self._placeholderAction,
            "Customize Model Architecture": self._placeholderAction,
            "Set Training Schedule": self._placeholderAction,
        }

        data_handling = {
            "Import Data": self._placeholderAction,
            "Preview Data": self._placeholderAction,
            "Clear Output": self._placeholderAction,
        }

        visualization_monitoring = {
            "Refresh GPU (CUDA) Check": self.checkCUDACallback,
            "Generate Conversation": self._requestGenerateConversation,
            "Visualize Training": self._placeholderAction,
            "Export Logs": self._placeholderAction,
        }

        utility = {
            "Reset to Defaults": self._placeholderAction,
            "Help/Documentation": self._placeholderAction,
        }

        self._createActionGroup(model_operations, "Model Operations")
        self._createActionGroup(data_handling, "Data Handling")
        self._createActionGroup(visualization_monitoring, "Visualization and Monitoring")
        self._createActionGroup(utility, "Utility")

    def _createActionGroup(self, action_dict, group_title):
        frame = tk.Frame(self, bg='#333333')
        frame.pack(fill=tk.X, padx=10, pady=5)
        title = StylizedTitle(frame, group_title, textColor=self.textColor, bgColor='#333333')
        title.pack(fill=tk.X)
        for action_text, action_callback in action_dict.items():
            button_fg_color = self.textColor if action_callback is not self._placeholderAction else '#555555'
            button_state = 'normal' if action_callback is not self._placeholderAction else 'disabled'
            button = tk.Button(frame, text=action_text, bg='#232323', fg=button_fg_color, 
                               command=action_callback, state=button_state, font=self.font)
            button.pack(fill=tk.X)

    def _placeholderAction(self):
        pass
        
    def _requestGenerateConversation(self):
        self.updateStatusCallback("Generating Conversation...")
        threading.Thread(target=self._backgroundGenerateConversation).start()

    def _backgroundGenerateConversation(self):
        response = requests.get(f"{self.backendURL}/generate_conversation")
        if response.ok:
            generatedText = response.json().get('conversation', '')
            self.after(0, lambda: self.drawGeneratedConversationCallback(generatedText))
            self.updateStatusCallback("Ready")
        else:
            self.after(0, lambda: self.updateStatusCallback("Error"))
