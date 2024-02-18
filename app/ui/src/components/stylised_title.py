import tkinter as tk

class StylizedTitle(tk.Frame):
    def __init__(self, parent, text, textColor="#00FFFF", bgColor="#333333", font=('Helvetica', 16, 'bold'), *args, **kwargs):
        super().__init__(parent, bg=bgColor, *args, **kwargs)
        
        # Top decoration line
        topLine = tk.Frame(self, bg=textColor, height=2)
        topLine.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Title label
        titleLabel = tk.Label(self, text=text, anchor="w", bg=bgColor, fg=textColor, font=font)
        titleLabel.pack(fill=tk.X, padx=10, pady=(5, 5))
        
        # Bottom decoration line
        bottomLine = tk.Frame(self, bg=textColor, height=2)
        bottomLine.pack(fill=tk.X, padx=10, pady=(0, 10))
