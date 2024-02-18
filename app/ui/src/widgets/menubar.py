import tkinter as tk

class MenuBar:
    def __init__(self, master, textColor, changeTextColorCallback):
        self.master = master
        self.textColor = textColor
        self.changeTextColorCallback = changeTextColorCallback
        self.menuBar = self._setupMenuBar()

    def _setupMenuBar(self):
        menuBar = tk.Menu(self.master, bg='#333333', fg=self.textColor)
        self.master.config(menu=menuBar)

        textColorMenu = tk.Menu(menuBar, tearoff=0, bg='#333333', fg=self.textColor)
        menuBar.add_cascade(label="Text Color", menu=textColorMenu)

        textColorMenu.add_command(label="Green", command=lambda: self.changeTextColorCallback('#00FF00'))
        textColorMenu.add_command(label="Cyan", command=lambda: self.changeTextColorCallback('#00FFFF'))
        textColorMenu.add_command(label="Bright Pink", command=lambda: self.changeTextColorCallback('#FF00FF'))

        return menuBar

    def get_menu_bar(self):
        return self.menuBar

