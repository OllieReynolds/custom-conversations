import tkinter as tk

class ConfigurationEditorFrame(tk.Frame):
    def __init__(self, parent, textColor, backendURL, *args, **kwargs):
        super().__init__(parent, bg='#333333', *args, **kwargs)
        self.textColor = textColor
        self.backendURL = backendURL
        self._setup_ui()

    def _setup_ui(self):
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
            ("Model Directory", "model_directory", "../models/smut"),
            ("Model Name", "model_name", "gpt2"),
            ("File Path", "file_path", ""),
            ("Device", "device", "cuda"),
            ("Max Length Increment", "max_length_increment", 500),
            ("Do Sample", "do_sample", True),
            ("Top K", "top_k", 50),
            ("No Repeat Ngram Size", "no_repeat_ngram_size", 2),
            ("Temperature", "temperature", 0.8),
            ("Top P", "top_p", 0.92),
            ("Num Train Epochs", "num_train_epochs", 20),
            ("Per Device Train Batch Size", "per_device_train_batch_size", 16),
            ("Gradient Accumulation Steps", "gradient_accumulation_steps", 1),
            ("FP16", "fp16", True),
            ("Learning Rate", "learning_rate", 3e-5),
            ("Warmup Steps", "warmup_steps", 1000),
            ("Save Steps", "save_steps", 10000),
            ("Save Total Limit", "save_total_limit", 2),
            ("Evaluation Strategy", "evaluation_strategy", "steps"),
            ("Eval Steps", "eval_steps", 1000)
        ]

        self.config_entries = {}
        for idx, (label_text, key, default) in enumerate(config_options):
            label = tk.Label(scrollable_frame, text=label_text, bg='#333333', fg=self.textColor)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky='w')

            entry_var = tk.StringVar(value=str(default))
            entry = tk.Entry(scrollable_frame, textvariable=entry_var, bg='#232323', fg=self.textColor)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
            self.config_entries[key] = entry_var

        applyButton = tk.Button(scrollable_frame, text="Apply Changes", bg='#232323', fg=self.textColor)
        applyButton.grid(row=len(config_options), column=0, columnspan=2, pady=10)