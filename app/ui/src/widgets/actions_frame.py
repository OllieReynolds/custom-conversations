import tkinter as tk

class ActionFrame(tk.Frame):
    def __init__(self, parent, textColor, backendURL, checkCUDACallback, *args, **kwargs):
        super().__init__(parent, bg='#333333', *args, **kwargs)
        self.textColor = textColor
        self.backendURL = backendURL
        self.checkCUDACallback = checkCUDACallback
        self._createWidgets()

    def _createWidgets(self):
        refreshButton = tk.Button(self, text="Refresh GPU (CUDA) Check", bg='#232323', fg=self.textColor, command=self.checkCUDACallback)
        refreshButton.pack(fill=tk.X, padx=10, pady=5)
        
        retrainModel = tk.Button(self, text="Retrain Model", bg='#232323', fg=self.textColor)
        retrainModel.pack(fill=tk.X, padx=10, pady=5)
