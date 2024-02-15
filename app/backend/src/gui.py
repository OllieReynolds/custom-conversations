import tkinter as tk
from tkinter import scrolledtext
import threading
import torch
from app import generate_conversation
from utils import check_cuda_available

class ConversationGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversation Generator")
        self._configure_ui()
        self._configure_tags()
        self.update_cuda_indicator()

    def _configure_ui(self):
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self._setup_cuda_frame()
        self._setup_generation_frame()

    def _setup_cuda_frame(self):
        frame_cuda = tk.Frame(self.paned_window)
        self.cuda_indicator_label = tk.Label(frame_cuda, text="", font=("Helvetica", 10))
        self.cuda_indicator_label.pack(fill=tk.X)
        refresh_cuda_button = tk.Button(frame_cuda, text="Refresh GPU (CUDA) Check", command=self.update_cuda_indicator)
        refresh_cuda_button.pack(fill=tk.X)
        self.paned_window.add(frame_cuda)

    def _setup_generation_frame(self):
        frame_gen_conversation = tk.Frame(self.paned_window)
        self.text_area = scrolledtext.ScrolledText(frame_gen_conversation, wrap=tk.WORD, state='disabled')
        self.text_area.pack(fill=tk.BOTH, expand=True)
        generate_button = tk.Button(frame_gen_conversation, text="Generate Conversation", command=self.start_conversation_generation)
        generate_button.pack(fill=tk.X)
        self.spinner_label = tk.Label(frame_gen_conversation, text="Ready", font=("Helvetica", 10))
        self.spinner_label.pack(fill=tk.X)
        self.paned_window.add(frame_gen_conversation)

    def _configure_tags(self):
        self.text_area.tag_config('speaker1', background='lightgrey')
        self.text_area.tag_config('speaker2', background='white')

    def update_cuda_indicator(self):
        cuda_available = check_cuda_available()
        cuda_text = "GPU (CUDA): Available" if cuda_available else "GPU (CUDA): Not Available"
        cuda_color = "green" if cuda_available else "red"
        self.cuda_indicator_label.config(text=cuda_text, fg=cuda_color)

    def start_conversation_generation(self):
        self.spinner_label.config(text="Working...")
        threading.Thread(target=self.generate_conversation_thread).start()

    def generate_conversation_thread(self):
        generated_text = generate_conversation()
        self.text_area.after(0, self.update_conversation, generated_text)
        self.text_area.after(0, self.stop_spinner)

    def update_conversation(self, generated_text):
        self.text_area.configure(state='normal')
        speakers = {}
        current_tag = None
        last_speaker = None

        for line in generated_text.split('\n'):
            if ':' in line:
                speaker, message = line.split(':', 1)
                if speaker not in speakers:
                    speakers[speaker] = f"speaker{len(speakers) % 2 + 1}"
                current_tag = speakers[speaker]
                if speaker != last_speaker:
                    self.text_area.insert(tk.END, line + '\n', current_tag)
                    last_speaker = speaker
            else:
                self.text_area.insert(tk.END, line + '\n', current_tag)

        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)
        self.spinner_label.config(text="Ready")

    def stop_spinner(self):
        self.spinner_label.config(text="Ready")

if __name__ == "__main__":
    app = ConversationGenerator()
    app.mainloop()