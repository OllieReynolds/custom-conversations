import tkinter as tk

class ActionPanelStylizedTitle(tk.Frame):
    def __init__(self, parent, text, textColor="#CCCCCC", bgColor="#333333", font=('Helvetica', 10, 'bold'), *args, **kwargs):
        super().__init__(parent, bg=bgColor, *args, **kwargs)
        
        # Title label
        titleLabel = tk.Label(self, text=text, anchor="w", bg=bgColor, fg=textColor, font=font)
        titleLabel.pack(fill=tk.X, padx=(20, 10), pady=(2, 2))
        
        # Subtle underline decoration
        underline = tk.Frame(self, bg=textColor, height=1, relief='flat')
        underline.pack(fill=tk.X, padx=(20, 10), pady=(0, 5))
