import tkinter as tk
from tkinter import font as tkfont
from app.ui.src.services.cuda import CUDAService
from app.ui.src.theme_manager import ThemeManager
from app.ui.src.utils import dark_title_bar
from app.ui.src.widgets.actions_frame import ActionFrame
from app.ui.src.widgets.configuration_editor import ConfigurationEditorFrame
from app.ui.src.widgets.generate_conversation import GenerateConversationFrame
from app.ui.src.widgets.menubar import MenuBar
from app.ui.src.widgets.status_bar import StatusBarFrame

class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.colors = {'bg': '#121212', 'text': '#00FFFF'}
        self.defaultFont = tkfont.Font(family="Helvetica", size=12)
        self.setup_attrs()
        self._setup_ui()
        self.cudaService.checkCUDAAvailability(self.statusBar.updateCUDAStatus)

    def setup_attrs(self):
        self.configure(bg=self.colors['bg'])
        self.title("Conversation Generator")
        self.backendURL = "http://localhost:5000"
        self.cudaService = CUDAService(self.backendURL)
        self.statusBar = StatusBarFrame(self, textColor=self.colors['text'])
        self.state('zoomed')

    def _setup_ui(self):
        self.windowPane = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.colors['bg'], sashrelief=tk.RAISED, sashwidth=5)
        self.windowPane.pack(fill=tk.BOTH, expand=True)
        self.add_frames()
        self.themeManager = ThemeManager(self)
        self.menuBar = MenuBar(self, self.colors['text'], self.themeManager.changeTextColor)
        self.config(menu=self.menuBar.get_menu_bar())
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        dark_title_bar(self)

    def add_frames(self):
        self.generateConversationFrame = GenerateConversationFrame(self.windowPane, self.colors['text'], self.cudaService, font=self.defaultFont)
        checkCUDACallback = lambda: self.cudaService.checkCUDAAvailability(self.statusBar.updateCUDAStatus)

        self.actionFrame = ActionFrame(self.windowPane, self.colors['text'], self.cudaService, checkCUDACallback, self.statusBar.updateStatus, self.generateConversationFrame._drawGeneratedConversation, font=self.defaultFont)
        
        self.windowPane.add(self.actionFrame)
        self.windowPane.add(self.generateConversationFrame)
        self.windowPane.add(ConfigurationEditorFrame(self.windowPane, self.colors['text'], self.cudaService, font=self.defaultFont))

if __name__ == "__main__":
    app = AppUI()
    app.mainloop()
