import tkinter as tk
from tkinter import scrolledtext
import threading
import requests

from app.ui.src.components.stylised_title import StylizedTitle

class GenerateConversationFrame(tk.Frame):
    def __init__(self, parent, textColor, backendURL, font=None, *args, **kwargs):
        super().__init__(parent, bg='#333333', *args, **kwargs)
        self.textColor = textColor
        self.backendURL = backendURL

        self.font=font
        self._setup_ui()

    def _setup_ui(self):
        title = StylizedTitle(self, "Conversation Output", textColor=self.textColor, bgColor='#333333')
        title.pack(fill=tk.X)
        self.textArea = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', bg='#121212', fg=self.textColor)
        self.textArea.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def _drawGeneratedConversation(self, generatedText):
        self.textArea.configure(state='normal')
        self.textArea.delete(1.0, tk.END)
        self.textArea.insert(tk.END, generatedText)
        self.textArea.configure(state='disabled')

