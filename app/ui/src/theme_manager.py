import tkinter as tk

class ThemeManager:
    def __init__(self, app):
        self.app = app

    def changeTextColor(self, color):
        self.app.textColor = color
        self._updateWidgetColors(self.app, color)

    def _updateWidgetColors(self, parent, color):
        for widget in parent.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
                widget.config(fg=color)
            if isinstance(widget, (tk.Frame, tk.PanedWindow, tk.Canvas, tk.LabelFrame)):
                self._updateWidgetColors(widget, color)
