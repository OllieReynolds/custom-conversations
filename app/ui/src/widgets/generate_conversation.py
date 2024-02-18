import tkinter as tk
from tkinter import scrolledtext
import threading
import requests

class GenerateConversationFrame(tk.Frame):
    def __init__(self, parent, textColor, backendURL, updateStatusCallback, *args, **kwargs):
        super().__init__(parent, bg='#333333', *args, **kwargs)
        self.textColor = textColor
        self.backendURL = backendURL
        self.updateStatusCallback = updateStatusCallback
        self._setup_ui()

    def _setup_ui(self):
        self.textArea = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', bg='#121212', fg=self.textColor)
        self.textArea.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        genButton = tk.Button(self, text="Generate Conversation", bg='#232323', fg=self.textColor, command=self._requestGenerateConversation)
        genButton.pack(fill=tk.X, padx=10, pady=5)

    def _requestGenerateConversation(self):
        self.updateStatusCallback("Generating Conversation...")
        threading.Thread(target=self._backgroundGenerateConversation).start()

    def _backgroundGenerateConversation(self):
        response = requests.get(f"{self.backendURL}/generate_conversation")
        if response.ok:
            generatedText = response.json().get('conversation', '')
            self.after(0, self._drawGeneratedConversation, generatedText)
        else:
            self.after(0, lambda: self.updateStatusCallback("Error"))

    def _drawGeneratedConversation(self, generatedText):
        self.textArea.configure(state='normal')
        self.textArea.delete(1.0, tk.END)
        self.textArea.insert(tk.END, generatedText)
        self.textArea.configure(state='disabled')
        self.updateStatusCallback("Ready")
