import tkinter as tk
from tkinter import messagebox

from app.ui.src.components.stylised_title import StylizedTitle

class ConfigurationEditorFrame(tk.Frame):
    def __init__(self, parent, textColor, backendURL, font=None, *args, **kwargs):
        super().__init__(parent, bg='#333333', *args, **kwargs)
        self.textColor = textColor
        self.backendURL = backendURL
        self.font = font
        self._setup_ui()

    def _setup_ui(self):
        
        title = StylizedTitle(self, "Configuration", textColor=self.textColor, bgColor='#333333')
        title.pack(fill=tk.X)
        
        canvas = tk.Canvas(self, bg='#333333')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        scrollable_frame = tk.Frame(canvas, bg='#333333')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        config_options = [
            ("Model Directory", "model_directory", "../models/smut", "The folder where AI models are stored. Changing this allows you to use different sets of AI models for text generation. Choose a directory path that is easily accessible and well-organized for efficient model management."),
            ("Model Name", "model_name", "gpt2", "The specific AI model to use for generating text. Different models may excel in different types of text generation tasks. Select a model that aligns with your task requirements and computational resources."),
            ("File Path", "file_path", "", "The location of the file to be processed. Altering this path changes the input text for generation. Specify the file path accurately to ensure the correct input data for text generation."),
            ("Device", "device", "cuda", "The hardware used for running the AI model. Switching to a different device can affect performance and resource usage. Choose the appropriate device based on availability and compatibility with the AI framework."),
            ("Max Length Increment", "max_length_increment", 500, "The maximum increase in text length during generation. Adjusting this parameter can control the length of generated text. Increase for longer text outputs or decrease for shorter, more concise outputs."),
            ("Do Sample", "do_sample", True, "Whether to randomly sample from the AI model for text generation. Enabling sampling can produce more diverse text outputs. Set to 'True' for varied and creative text, or 'False' for deterministic outputs."),
            ("Top K", "top_k", 50, "Controls the randomness in text generation. Adjusting this parameter can influence the diversity of generated text. Increase to allow more diverse tokens or decrease for more deterministic outputs."),
            ("No Repeat Ngram Size", "no_repeat_ngram_size", 2, "Prevents repeating sequences of words in generated text. Changing this can improve the coherence of generated text. Increase to avoid repetitive phrases, but be mindful of memory consumption."),
            ("Temperature", "temperature", 0.8, "Controls the degree of randomness in text generation. Adjusting this parameter can make the generated text more or less creative. Increase for more diverse and creative outputs, or decrease for more conservative and predictable text."),
            ("Top P", "top_p", 0.92, "The threshold for token selection during text generation. Changing this can influence the diversity and quality of generated text. Increase to include more diverse tokens or decrease for more selective outputs."),
            ("Num Train Epochs", "num_train_epochs", 20, "The number of cycles the AI model undergoes during training. Increasing this can lead to better model performance but also requires more computational resources. Increase for improved model convergence and performance, but consider computational costs."),
            ("Per Device Train Batch Size", "per_device_train_batch_size", 16, "The number of data samples processed per hardware device during training. Adjusting this parameter affects training speed and memory usage. Increase for faster training but monitor memory usage."),
            ("Gradient Accumulation Steps", "gradient_accumulation_steps", 1, "The number of steps for aggregating gradient updates during training. Changing this parameter can affect training stability and memory usage. Increase to reduce memory usage but monitor training stability."),
            ("FP16", "fp16", True, "Whether to use mixed precision training, which can speed up training. Enabling this can significantly reduce training time on supported hardware. Set to 'True' for faster training on compatible hardware."),
            ("Learning Rate", "learning_rate", 3e-5, "The rate at which the AI model adjusts during training. Modifying this parameter can affect the convergence speed and stability of training. Adjust cautiously for optimal model convergence."),
            ("Warmup Steps", "warmup_steps", 1000, "The initial steps where the learning rate is adjusted during training. Adjusting this can help stabilize training and improve convergence. Increase for smoother learning rate adjustments, especially in complex models."),
            ("Save Steps", "save_steps", 10000, "Interval steps for saving checkpoints of the AI model during training. Changing this affects the frequency of model saving and disk usage. Increase for less frequent but larger checkpoints, balancing disk space and checkpoint granularity."),
            ("Save Total Limit", "save_total_limit", 2, "The maximum number of saved checkpoints. Adjusting this parameter controls the disk space usage for saving model checkpoints. Increase to retain more checkpoints for model recovery and analysis."),
            ("Evaluation Strategy", "evaluation_strategy", "steps", "The method used for evaluating the AI model during training. Changing this can affect the training monitoring and evaluation process. Choose 'steps' for evaluation at fixed intervals during training."),
            ("Eval Steps", "eval_steps", 1000, "Interval steps for evaluating the AI model during training. Modifying this parameter affects the frequency of model evaluation during training. Increase for more frequent evaluations, especially in long training runs.")
        ]


        self.config_entries = {}
        for idx, (label_text, key, default, tooltip) in enumerate(config_options):
            label = tk.Label(scrollable_frame, text=label_text, bg='#333333', fg=self.textColor, font=self.font)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky='w')

            entry_var = tk.StringVar(value=str(default))
            entry = tk.Entry(scrollable_frame, textvariable=entry_var, bg='#232323', fg=self.textColor, font=self.font)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
            self.config_entries[key] = entry_var

            info_frame = tk.Frame(scrollable_frame, bg="#333333")
            info_frame.grid(row=idx, column=2, padx=5)

            info_icon = tk.Label(info_frame, text="i", bg='#333333', fg=self.textColor, cursor="question_arrow", font=self.font)
            info_icon.pack()
            info_icon.bind("<Button-1>", lambda event, tooltip=tooltip: self._show_tooltip(event, tooltip))

        applyButton = tk.Button(scrollable_frame, text="Apply Changes", bg='#232323', fg=self.textColor, font=self.font)
        applyButton.grid(row=len(config_options), column=0, columnspan=3, pady=10)

    def _show_tooltip(self, event, tooltip):
        messagebox.showinfo("Tooltip", tooltip)
