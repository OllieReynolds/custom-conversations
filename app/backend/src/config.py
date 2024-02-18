import torch
import os

class Config:
    def __init__(self, **kwargs):
        self.model_directory = kwargs.get('model_directory', "../models/smut")
        self.model_name = kwargs.get('model_name', "gpt2")
        self.file_path = kwargs.get('file_path', os.path.join(os.path.dirname(os.path.abspath(__file__)), '../input/smut.txt'))
        self.device = kwargs.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        
        # Generation parameters
        self.max_length_increment = kwargs.get('max_length_increment', 500)
        self.do_sample = kwargs.get('do_sample', True)
        self.top_k = kwargs.get('top_k', 50)
        self.no_repeat_ngram_size = kwargs.get('no_repeat_ngram_size', 2)
        self.temperature = kwargs.get('temperature', 0.8)
        self.top_p = kwargs.get('top_p', 0.92)
        
        # Training parameters
        self.num_train_epochs = kwargs.get('num_train_epochs', 20)
        self.per_device_train_batch_size = kwargs.get('per_device_train_batch_size', 16)
        self.gradient_accumulation_steps = kwargs.get('gradient_accumulation_steps', 1)
        self.fp16 = kwargs.get('fp16', True)
        self.learning_rate = kwargs.get('learning_rate', 3e-5)
        self.warmup_steps = kwargs.get('warmup_steps', 1000)
        self.save_steps = kwargs.get('save_steps', 10000)
        self.save_total_limit = kwargs.get('save_total_limit', 2)
        self.evaluation_strategy = kwargs.get('evaluation_strategy', 'steps')
        self.eval_steps = kwargs.get('eval_steps', 1000)

        # Required files setup
        self.required_files = ['config.json']
        
    def to_dict(self):
        return self.__dict__

