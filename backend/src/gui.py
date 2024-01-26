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
    # Disable the button to prevent multiple clicks
    generate_button.config(state=tk.DISABLED)
    # Start the spinner
    start_spinner()
    # Start a thread for the conversation generation process
    threading.Thread(target=generate_conversation_thread).start()

def generate_conversation_thread():
    generated_text = generate_conversation()  # This function should be defined in your app module
    # Once the conversation is generated, update the GUI from the main thread
    text_area.after(0, update_conversation, generated_text)
    # Stop the spinner and re-enable the button
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
    spinner_label.grid(column=0, row=2, pady=10)

def stop_spinner():
    spinner_label.grid_forget()

# Set up the main window
root = tk.Tk()
root.title("Conversation Generator")

# Configure grid to auto-expand
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create a scrolled text area widget
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
text_area.grid(column=0, row=0, sticky='nswe', pady=10, padx=10)

# Configure tags for alternating background colors
text_area.tag_config('speaker1', background='lightgrey')
text_area.tag_config('speaker2', background='white')

# Create a CUDA availability indicator label
cuda_indicator_label = tk.Label(root, text="", font=("Helvetica", 10))
cuda_indicator_label.grid(column=0, row=2, pady=10)

# Add a button to refresh the CUDA status
refresh_cuda_button = tk.Button(root, text="Refresh GPU (CUDA) Check", command=update_cuda_indicator)
refresh_cuda_button.grid(column=0, row=3, pady=10, padx=10, sticky='ew')

# Update the CUDA indicator label for the first time
update_cuda_indicator()

# Create a button to trigger conversation generation
generate_button = tk.Button(root, text="Generate Conversation", command=start_conversation_generation)
generate_button.grid(column=0, row=1, pady=10, padx=10, sticky='ew')

# Label used as a spinner
spinner_label = tk.Label(root, text="", font=("Helvetica", 10))

# Start the GUI event loop
root.mainloop()
