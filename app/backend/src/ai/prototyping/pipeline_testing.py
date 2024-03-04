import tkinter as tk
from tkinter import scrolledtext, ttk
from transformers import pipeline

# Define the GUI layout and logic
class TransformersGUI(tk.Tk):
    def __init__(self, pipelines_info):
        super().__init__()
        self.title("Hugging Face Transformers GUI")

        self.pipelines_info = pipelines_info
        self.pipeline_options = tk.StringVar(self)
        self.pipeline_options.set("Feature Extraction")
        self.create_widgets()
        
    def execute_pipeline(self):
        selected_pipeline = self.pipeline_options.get()
        self.input_text = self.input_text_area.get("1.0", tk.END).strip()

        # Initialize the result variable
        result = "Processing..."

        if selected_pipeline == 'Feature Extraction':
            feature_extraction = pipeline("feature-extraction")
            result = feature_extraction(self.input_text)[0][0][:5]  # Displaying first 5 features of the first token

        elif selected_pipeline == 'Fill-Mask':
            fill_mask = pipeline("fill-mask")
            result = fill_mask(self.input_text)

        elif selected_pipeline == 'NER':
            ner = pipeline("ner")
            result = ner(self.input_text)

        elif selected_pipeline == 'Question Answering':
            # For simplicity, let's assume the question is the first sentence and the context is the rest
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

        # Display the result in the result text area
        self.result_text_area.config(state=tk.NORMAL)
        self.result_text_area.delete('1.0', tk.END)
        self.result_text_area.insert('1.0', str(result))
        self.result_text_area.config(state=tk.DISABLED)

    # Function to update the information pane
    def update_info_pane(self, *args):
        selected_pipeline = self.pipeline_options.get()
        info = pipelines_info[selected_pipeline]
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
    pipelines_info = {
        "Feature Extraction": {
            "description": "Extracts the underlying features from the text.",
            "usage": "Used in text analysis, to understand underlying patterns.",
            "sample_input": "Hello, world!",
            "expected_output": "A vector representation of the text."
        },
        "Fill-Mask": {
            "description": "Predicts the missing word in a sentence.",
            "usage": "Can be used for data augmentation or to guess missing words.",
            "sample_input": "Hello, I'm a [MASK] model.",
            "expected_output": "Predicted word for the mask."
        },
        "NER": {
            "description": "Identifies entities in the text like names, locations, dates.",
            "usage": "Used in information extraction to identify and classify named entities.",
            "sample_input": "Albert Einstein was born in Ulm.",
            "expected_output": "Albert Einstein: Person, Ulm: Location"
        },
        "Question Answering": {
            "description": "Answers questions based on the context provided.",
            "usage": "Useful for building automated FAQ or information retrieval systems.",
            "sample_input": "Context: Python is a programming language. Question: What is Python?",
            "expected_output": "Answer: a programming language"
        },
        "Sentiment Analysis": {
            "description": "Determines if the sentiment is positive, negative, or neutral.",
            "usage": "Commonly used in analyzing customer feedback, social media.",
            "sample_input": "I love this phone!",
            "expected_output": "Positive sentiment"
        },
        "Summarization": {
            "description": "Provides a summary of the input text.",
            "usage": "Helpful for condensing large texts into shorter summaries.",
            "sample_input": "The quick brown fox jumps over the lazy dog.",
            "expected_output": "A concise summary of the text."
        },
        "Text Generation": {
            "description": "Generates text based on the input.",
            "usage": "Can be used for content creation, chatbots, and more.",
            "sample_input": "Once upon a time,",
            "expected_output": "Continuation of the text."
        },
        "Translation (EN to FR)": {
            "description": "Translates English text to French.",
            "usage": "Useful for translating content between languages.",
            "sample_input": "Hello, world!",
            "expected_output": "Bonjour le monde!"
        },
        "Zero-Shot Classification": {
            "description": "Classifies text without needing explicit examples for training.",
            "usage": "Useful for classifying text into predefined categories.",
            "sample_input": "This is a course about AI.",
            "expected_output": "Categories: Education, Technology"
        }
    }
    app = TransformersGUI(pipelines_info)
    app.mainloop()