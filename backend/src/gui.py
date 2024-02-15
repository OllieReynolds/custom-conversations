import tkinter as tk
from tkinter import scrolledtext
import threading
from app import generate_conversation
import torch

def update_cuda_indicator():
    cuda_available = torch.cuda.is_available()
    cuda_text = "GPU (CUDA): Available" if cuda_available else "GPU (CUDA): Not Available"
    cuda_color = "green" if cuda_available else "red"
    cuda_indicator_label.config(text=cuda_text, fg=cuda_color)

def start_conversation_generation():
    generate_button.config(state=tk.DISABLED)
    start_spinner()
    threading.Thread(target=generate_conversation_thread).start()

def generate_conversation_thread():
    generated_text = generate_conversation()
    text_area.after(0, update_conversation, generated_text)
    text_area.after(0, stop_spinner)

def update_conversation(generated_text):
    text_area.configure(state='normal')
    speakers = {}
    current_tag = None
    last_speaker = None

    for line in generated_text.split('\n'):
        if ':' in line:
            speaker = line.split(':', 1)[0]
            if speaker not in speakers:
                speakers[speaker] = f"speaker{len(speakers) % 2 + 1}"
            current_tag = speakers[speaker]
            if speaker != last_speaker:
                text_area.insert(tk.END, line + '\n', current_tag)
                last_speaker = speaker
        else:
            text_area.insert(tk.END, line + '\n', current_tag)

    text_area.configure(state='disabled')
    text_area.see(tk.END)  # Auto-scrolls to the end of the text area
    generate_button.config(state=tk.NORMAL)  # Re-enable the button

def start_spinner():
    spinner_label.config(text="Working...")
    spinner_label.pack(fill=tk.X)

def stop_spinner():
    spinner_label.config(text="Ready")
    spinner_label.pack(fill=tk.X)

# Set up the main window
root = tk.Tk()
root.title("Conversation Generator")

paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

frame_cuda = tk.Frame(paned_window)
cuda_indicator_label = tk.Label(frame_cuda, text="", font=("Helvetica", 10))
cuda_indicator_label.pack(fill=tk.X)
refresh_cuda_button = tk.Button(frame_cuda, text="Refresh GPU (CUDA) Check", command=update_cuda_indicator)
refresh_cuda_button.pack(fill=tk.X)

paned_window.add(frame_cuda)

frame_gen_conversation = tk.Frame(paned_window)
text_area = scrolledtext.ScrolledText(frame_gen_conversation, wrap=tk.WORD, state='disabled')
text_area.tag_config('speaker1', background='lightgrey')
text_area.tag_config('speaker2', background='white')
text_area.pack(fill=tk.BOTH, expand=True)
generate_button = tk.Button(frame_gen_conversation, text="Generate Conversation", command=start_conversation_generation)
generate_button.pack(fill=tk.X)
spinner_label = tk.Label(frame_gen_conversation, text="Ready", font=("Helvetica", 10))
spinner_label.pack(fill=tk.X)

paned_window.add(frame_gen_conversation)

# Update the CUDA indicator label for the first time
update_cuda_indicator()

# Start the GUI event loop
root.mainloop()
