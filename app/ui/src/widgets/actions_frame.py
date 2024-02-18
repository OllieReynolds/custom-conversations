import threading
import tkinter as tk

import requests

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
        
        refreshButton = tk.Button(self, text="Refresh GPU (CUDA) Check", bg='#232323', fg=self.textColor, command=self.checkCUDACallback, font=self.font)
        refreshButton.pack(fill=tk.X, padx=10, pady=5)
        
        retrainModel = tk.Button(self, text="Retrain Model", bg='#232323', fg=self.textColor, font=self.font)
        retrainModel.pack(fill=tk.X, padx=10, pady=5)
        
        genButton = tk.Button(self, text="Generate Conversation", bg='#232323', fg=self.textColor, command=self._requestGenerateConversation, font=self.font)
        genButton.pack(fill=tk.X, padx=10, pady=5)
        
        
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