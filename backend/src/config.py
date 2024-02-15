import torch
import os

class Config:
    def __init__(self, model_directory="../trained_model", model_name="gpt2"):
        # Change the working directory to the backend directory
        backend_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(backend_directory)
        
        self.model_directory = model_directory
        self.required_files = ['config.json']
        self.model_name = model_name
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../input', 'matthew_processed.txt')
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

