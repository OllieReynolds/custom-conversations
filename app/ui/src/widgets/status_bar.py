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

        # Customization for cool-looking status bar
        self.cudaIcon.config(font=("Arial", 16), fg='#FFD700')  # Change CUDA icon font and color
        self.cudaStatus.config(font=("Helvetica", 10, 'italic'), fg='#00FF00')  # Change CUDA status font, style, and color
        self.statusLabel.config(font=("Arial", 10, 'bold'), fg='#00FFFF')  # Change status label font, style, and color

    def updateStatus(self, text):
        self.statusLabel.config(text=text)
        
    def updateCUDAStatus(self, isAvailable):
        cudaText = "GPU (CUDA): Available" if isAvailable else "GPU (CUDA): Not Available"
        cudaColor = "#00FF00" if isAvailable else "#FF0000"
        self.cudaStatus.config(text=cudaText, fg=cudaColor)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x100")
    statusBar = StatusBarFrame(root)
    statusBar.updateStatus("Processing...")
    statusBar.updateCUDAStatus(True)
    root.mainloop()
