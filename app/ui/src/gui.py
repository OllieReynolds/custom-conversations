import tkinter as tk
from tkinter import scrolledtext
import requests
import threading

class ConversationGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversation Generator")
        self.backend_url = "http://localhost:5000"
        self._configure_ui()
        self.req_check_cuda_available()

    def _configure_ui(self):
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self._setup_check_cuda_frame()
        self._setup_generate_conversation_frame()
        self._setup_status_bar_frame()

    def _setup_check_cuda_frame(self):
        frame_cuda = tk.Frame(self.paned_window)
        refresh_cuda_button = tk.Button(frame_cuda, text="Refresh GPU (CUDA) Check", command=self.req_check_cuda_available)
        refresh_cuda_button.pack(fill=tk.X, padx=10, pady=5)
        self.paned_window.add(frame_cuda)

    def _setup_generate_conversation_frame(self):
        frame_gen_conversation = tk.Frame(self.paned_window)
        self.text_area = scrolledtext.ScrolledText(frame_gen_conversation, wrap=tk.WORD, state='disabled')
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        generate_button = tk.Button(frame_gen_conversation, text="Generate Conversation", command=self.req_generate_conversation)
        generate_button.pack(fill=tk.X, padx=10, pady=5)
        self.paned_window.add(frame_gen_conversation)

    def _setup_status_bar_frame(self):
        self.status_frame = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # CUDA indicator
        self.cuda_icon = tk.Label(self.status_frame, text="\u2699", font=("Arial", 12))
        self.cuda_icon.grid(row=0, column=0, padx=(10,0), pady=5)

        self.cuda_indicator_label = tk.Label(self.status_frame, text="Checking GPU (CUDA)...", font=("Helvetica", 10))
        self.cuda_indicator_label.grid(row=0, column=1, padx=(0,10), pady=5, sticky='w')

        # Spinner
        self.spinner_label = tk.Label(self.status_frame, text="Ready")
        self.spinner_label.grid(row=0, column=2, padx=(0,10), pady=5, sticky='e')

    def req_check_cuda_available(self):
        threading.Thread(target=self._background_check_cuda_available).start()

    def req_generate_conversation(self):
        self.spinner_label.config(text="Generating Conversation...")
        threading.Thread(target=self._background_generate_conversation).start()

    def _background_check_cuda_available(self):
        response = requests.get(f"{self.backend_url}/check_cuda_available")
        if response.ok:
            cuda_available = response.json().get('cuda_available', False)
            self.after(0, self.draw_check_cuda_available, cuda_available)
        else:
            self.after(0, self.draw_check_cuda_available, False)

    def _background_generate_conversation(self):
        response = requests.get(f"{self.backend_url}/generate_conversation")
        if response.ok:
            generated_text = response.json().get('conversation', '')
            self.after(0, self.draw_generate_conversation, generated_text)
        else:
            self.after(0, lambda: self.spinner_label.config(text="Error"))

    def draw_check_cuda_available(self, is_available):
        cuda_text = "GPU (CUDA): Available" if is_available else "GPU (CUDA): Not Available"
        cuda_color = "green" if is_available else "red"
        self.cuda_indicator_label.config(text=cuda_text, fg=cuda_color)

    def draw_generate_conversation(self, generated_text):
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, generated_text)
        self.text_area.configure(state='disabled')
        self.spinner_label.config(text="Ready")

if __name__ == "__main__":
    ui = ConversationGenerator()
    ui.mainloop()
