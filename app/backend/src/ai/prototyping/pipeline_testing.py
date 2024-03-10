import tkinter as tk
from tkinter import scrolledtext, ttk
from transformers import pipeline
import json
import os

class TransformersGUI(tk.Tk):
    def __init__(self, pipelines_info_file):
        super().__init__()
        self.title("Hugging Face Transformers GUI")

        current_dir = os.path.dirname(__file__)
        full_path = os.path.join(current_dir, pipelines_info_file)
        
        with open(full_path, 'r') as file:
            self.pipelines_info = json.load(file)

        if not isinstance(self.pipelines_info, dict):
            raise ValueError("pipelines_info must be a dictionary")

        self.pipeline_options = tk.StringVar(self)
        self.pipeline_options.set(next(iter(self.pipelines_info)))  
        self.create_widgets()
        
    def execute_pipeline(self):
        selected_pipeline = self.pipeline_options.get()
        self.input_text = self.input_text_area.get("1.0", tk.END).strip()

        result = "Processing..."

        if selected_pipeline == 'Feature Extraction':
            feature_extraction = pipeline("feature-extraction")
            result = feature_extraction(self.input_text)[0][0][:5]

        elif selected_pipeline == 'Fill-Mask':
            fill_mask = pipeline("fill-mask")
            result = fill_mask(self.input_text)

        elif selected_pipeline == 'NER':
            ner = pipeline("ner")
            result = ner(self.input_text)

        elif selected_pipeline == 'Question Answering':
            parts = self.input_text.split('.', 1)
            question_answering = pipeline("question-answering")
            result = question_answering(question=parts[0], context=parts[1]) if len(parts) > 1 else "Invalid input format for QA."

        elif selected_pipeline == 'Sentiment Analysis':
            sentiment_analysis = pipeline("sentiment-analysis")
            result = sentiment_analysis(self.input_text)

        elif selected_pipeline == 'Summarization':
            summarization = pipeline("summarization")
            result = summarization(self.input_text)

        elif selected_pipeline == 'Text Generation':
            text_generation = pipeline("text-generation")
            result = text_generation(self.input_text, max_length=50)

        elif selected_pipeline == 'Translation (EN to FR)':
            translation = pipeline("translation_en_to_fr")
            result = translation(self.input_text)

        elif selected_pipeline == 'Zero-Shot Classification':
            zero_shot_classification = pipeline("zero-shot-classification")
            result = zero_shot_classification(self.input_text, candidate_labels=['education', 'politics', 'business'])

        self.result_text_area.config(state=tk.NORMAL)
        self.result_text_area.delete('1.0', tk.END)
        self.result_text_area.insert('1.0', str(result))
        self.result_text_area.config(state=tk.DISABLED)

    def update_info_pane(self, *args):
        selected_pipeline = self.pipeline_options.get()
        info = self.pipelines_info[selected_pipeline]
        info_text = f"Description: {info['description']}\n\n" \
                    f"Usage: {info['usage']}\n\n" \
                    f"Sample Input: {info['sample_input']}\n\n" \
                    f"Expected Output: {info['expected_output']}"
        self.info_text_area.config(state=tk.NORMAL)
        self.info_text_area.delete('1.0', tk.END)
        self.info_text_area.insert('1.0', info_text)
        self.info_text_area.config(state=tk.DISABLED)

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=0)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)

        pipeline_menu_label = ttk.Label(left_frame, text="Select a Pipeline:")
        pipeline_menu_label.pack(fill=tk.X, pady=(0, 5))

        pipeline_menu = ttk.OptionMenu(left_frame, self.pipeline_options, *self.pipelines_info.keys())
        pipeline_menu.pack(fill=tk.X)

        input_text_label = ttk.Label(left_frame, text="Input Text:")
        input_text_label.pack(fill=tk.X, pady=(10, 5))

        self.input_text_area = scrolledtext.ScrolledText(left_frame, height=10)
        self.input_text_area.pack(fill=tk.BOTH, expand=True)

        execute_button = ttk.Button(left_frame, text="Execute", command=self.execute_pipeline)
        execute_button.pack(fill=tk.X, pady=(5, 0))

        result_text_label = ttk.Label(left_frame, text="Result:")
        result_text_label.pack(fill=tk.X, pady=(10, 5))

        self.result_text_area = scrolledtext.ScrolledText(left_frame, height=10)
        self.result_text_area.pack(fill=tk.BOTH, expand=True)
        self.result_text_area.config(state=tk.DISABLED)

        self.info_text_area = scrolledtext.ScrolledText(right_frame, height=20)
        self.info_text_area.pack(fill=tk.BOTH, expand=True)
        self.info_text_area.config(state=tk.DISABLED)

        self.update_info_pane()
        
if __name__ == "__main__":
    pipelines_info_file = "pipelines_info.json"
    app = TransformersGUI(pipelines_info_file)
    app.mainloop()