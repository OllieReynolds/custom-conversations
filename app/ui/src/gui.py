import tkinter as tk
from tkinter import scrolledtext, Menu
import requests
import threading

from app.ui.src.utils import dark_title_bar

class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversation Generator")
        self.backendURL = "http://localhost:5000"
        self.configure(bg='#121212')
        self.textColor = '#FF00FF'
        self._configureUI()
        self._requestCheckCUDAAvailability()

    def _configureUI(self):
        self.windowPane = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg='#121212', sashrelief=tk.RAISED, sashwidth=5)
        self.windowPane.pack(fill=tk.BOTH, expand=True)

        self._setupCUDACheckFrame()
        self._setupConversationGenFrame()
        self._setupStatusBar()
        self._setupMenu()
        dark_title_bar(self)

    def _setupCUDACheckFrame(self):
        cudaFrame = tk.Frame(self.windowPane, bg='#333333')
        refreshButton = tk.Button(cudaFrame, text="Refresh GPU (CUDA) Check", bg='#232323', fg=self.textColor, command=self._requestCheckCUDAAvailability)
        refreshButton.pack(fill=tk.X, padx=10, pady=5)
        self.windowPane.add(cudaFrame)

    def _setupConversationGenFrame(self):
        convFrame = tk.Frame(self.windowPane, bg='#333333')
        self.textArea = scrolledtext.ScrolledText(convFrame, wrap=tk.WORD, state='disabled', bg='#121212', fg=self.textColor)
        self.textArea.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        genButton = tk.Button(convFrame, text="Generate Conversation", bg='#232323', fg=self.textColor, command=self._requestGenerateConversation)
        genButton.pack(fill=tk.X, padx=10, pady=5)
        self.windowPane.add(convFrame)

    def _setupStatusBar(self):
        statusBar = tk.Frame(self, bd=1, relief=tk.SUNKEN, bg='#333333')
        statusBar.pack(side=tk.BOTTOM, fill=tk.X)

        self.cudaIcon = tk.Label(statusBar, text="\u2699", font=("Arial", 12), bg='#333333', fg=self.textColor)
        self.cudaIcon.grid(row=0, column=0, padx=(10,0), pady=5)

        self.cudaStatus = tk.Label(statusBar, text="Checking GPU (CUDA)...", font=("Helvetica", 10), bg='#333333', fg=self.textColor)
        self.cudaStatus.grid(row=0, column=1, padx=(0,10), pady=5, sticky='w')

        self.statusLabel = tk.Label(statusBar, text="Ready", bg='#333333', fg=self.textColor)
        self.statusLabel.grid(row=0, column=2, padx=(0,10), pady=5, sticky='e')

    def _setupMenu(self):
        menuBar = Menu(self, bg='#333333', fg=self.textColor)
        self.config(menu=menuBar)

        textColorMenu = Menu(menuBar, tearoff=0, bg='#333333', fg=self.textColor)
        menuBar.add_cascade(label="Text Color", menu=textColorMenu)

        textColorMenu.add_command(label="Green", command=lambda: self._changeTextColor('#00FF00'))
        textColorMenu.add_command(label="Cyan", command=lambda: self._changeTextColor('#00FFFF'))
        textColorMenu.add_command(label="Bright Pink", command=lambda: self._changeTextColor('#FF00FF'))

    def _changeTextColor(self, color):
        self.textColor = color
        self.textArea.config(fg=color)
        self.cudaIcon.config(fg=color)
        self.cudaStatus.config(fg=color)
        self.statusLabel.config(fg=color)
        for widget in self.windowPane.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Button):
                    child.config(fg=color)

    def _requestCheckCUDAAvailability(self):
        threading.Thread(target=self._backgroundCheckCUDAAvailability).start()

    def _requestGenerateConversation(self):
        self.statusLabel.config(text="Generating Conversation...")
        threading.Thread(target=self._backgroundGenerateConversation).start()

    def _backgroundCheckCUDAAvailability(self):
        response = requests.get(f"{self.backendURL}/check_cuda_available")
        if response.ok:
            cudaAvailable = response.json().get('cuda_available', False)
            self.after(0, self._drawCUDAAvailability, cudaAvailable)
        else:
            self.after(0, self._drawCUDAAvailability, False)

    def _backgroundGenerateConversation(self):
        response = requests.get(f"{self.backendURL}/generate_conversation")
        if response.ok:
            generatedText = response.json().get('conversation', '')
            self.after(0, self._drawGeneratedConversation, generatedText)
        else:
            self.after(0, lambda: self.statusLabel.config(text="Error"))

    def _drawCUDAAvailability(self, isAvailable):
        cudaText = "GPU (CUDA): Available" if isAvailable else "GPU (CUDA): Not Available"
        cudaColor = "green" if isAvailable else "red"
        self.cudaStatus.config(text=cudaText, fg=cudaColor)

    def _drawGeneratedConversation(self, generatedText):
        self.textArea.configure(state='normal')
        self.textArea.delete(1.0, tk.END)
        self.textArea.insert(tk.END, generatedText)
        self.textArea.configure(state='disabled')
        self.statusLabel.config(text="Ready")

if __name__ == "__main__":
    app = AppUI()
    app.mainloop()
