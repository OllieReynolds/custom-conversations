import tkinter as tk

class StatusBarFrame(tk.Frame):
    def __init__(self, parent, bgColor='#333333', textColor='#FF00FF', *args, **kwargs):
        super().__init__(parent, bd=1, relief=tk.SUNKEN, bg=bgColor, *args, **kwargs)
        self.pack(side=tk.BOTTOM, fill=tk.X)
        self._createWidgets(textColor)

    def _createWidgets(self, textColor):
        self.cudaIcon = tk.Label(self, text="\u2699", font=("Arial", 12), bg='#333333', fg=textColor)
        self.cudaIcon.grid(row=0, column=0, padx=(10,0), pady=5)

        self.cudaStatus = tk.Label(self, text="Checking GPU (CUDA)...", font=("Helvetica", 10), bg='#333333', fg=textColor)
        self.cudaStatus.grid(row=0, column=1, padx=(0,10), pady=5, sticky='w')

        self.statusLabel = tk.Label(self, text="Ready", bg='#333333', fg=textColor)
        self.statusLabel.grid(row=0, column=2, padx=(0,10), pady=5, sticky='e')

    def updateStatus(self, text):
        self.statusLabel.config(text=text)
        
    def updateCUDAStatus(self, isAvailable):
        cudaText = "GPU (CUDA): Available" if isAvailable else "GPU (CUDA): Not Available"
        cudaColor = "green" if isAvailable else "red"
        self.cudaStatus.config(text=cudaText, fg=cudaColor)
