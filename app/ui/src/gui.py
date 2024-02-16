
import tkinter as tk
from tkinter import scrolledtext
from app.common.src.mqtt import MQTTService

class ConversationGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversation Generator")
        self.mqtt_service = MQTTService()
        self.mqtt_service.start()
        self.mqtt_setup()
        self._configure_ui()
        
    def mqtt_setup(self):
        self.mqtt_service.subscribe("rec/app/generate_conversation", self.draw_generate_conversation)
        self.mqtt_service.subscribe("rec/utils/check_cuda_available", self.draw_check_cuda_available)
        self.req_check_cuda_available()

    def _configure_ui(self):
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self._setup_check_cuda_frame()
        self._setup_generate_conversation_frame()
        self._setup_status_bar_frame()

    def _setup_check_cuda_frame(self):
        frame_cuda = tk.Frame(self.paned_window)
        self.cuda_indicator_label = tk.Label(frame_cuda, text="GPU (CUDA): Checking...", font=("Helvetica", 10))
        self.cuda_indicator_label.pack(fill=tk.X)
        refresh_cuda_button = tk.Button(frame_cuda, text="Refresh GPU (CUDA) Check", command=self.req_check_cuda_available)
        refresh_cuda_button.pack(fill=tk.X)
        self.paned_window.add(frame_cuda)

    def _setup_generate_conversation_frame(self):
        frame_gen_conversation = tk.Frame(self.paned_window)
        self.text_area = scrolledtext.ScrolledText(frame_gen_conversation, wrap=tk.WORD, state='disabled')
        self.text_area.tag_config('speaker1', background='lightgrey')
        self.text_area.tag_config('speaker2', background='white')
        self.text_area.pack(fill=tk.BOTH, expand=True)
        generate_button = tk.Button(frame_gen_conversation, text="Generate Conversation", command=self.req_generate_conversation)
        generate_button.pack(fill=tk.X)
        self.spinner_label = tk.Label(frame_gen_conversation, text="Ready", font=("Helvetica", 10))
        self.spinner_label.pack(fill=tk.X)
        self.paned_window.add(frame_gen_conversation)
        
    def _setup_status_bar_frame(self):
        self.status_frame = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Example of adding multiple labels and icons to the status bar
        self.status_label_1 = tk.Label(self.status_frame, text="Status: Ready", anchor=tk.W)
        self.status_label_1.pack(side=tk.LEFT)

        self.status_label_2 = tk.Label(self.status_frame, text="GPU: Not checked", anchor=tk.W)
        self.status_label_2.pack(side=tk.LEFT)

        # Assuming you have icon images named 'icon1.png', 'icon2.png' in the application directory
        # self.icon1 = tk.PhotoImage(file="icon1.png")
        # self.icon_label_1 = tk.Label(self.status_frame, image=self.icon1)
        # self.icon_label_1.pack(side=tk.LEFT)

        # self.icon2 = tk.PhotoImage(file="icon2.png")
        # self.icon_label_2 = tk.Label(self.status_frame, image=self.icon2)
        # self.icon_label_2.pack(side=tk.LEFT)

    def req_generate_conversation(self):
        self.spinner_label.config(text="Working...")
        self.mqtt_service.publish("req/app/generate_conversation", "request")
        
    def req_check_cuda_available(self):
        self.mqtt_service.publish("req/utils/check_cuda_available", "request")

    def draw_check_cuda_available(self, message):
        cuda_available = message == "True"
        cuda_text = "GPU (CUDA): Available" if cuda_available else "GPU (CUDA): Not Available"
        cuda_color = "green" if cuda_available else "red"
        self.cuda_indicator_label.config(text=cuda_text, fg=cuda_color)

    def draw_generate_conversation(self, generated_text):
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
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

if __name__ == "__main__":
    ui = ConversationGenerator()
    ui.mainloop()
