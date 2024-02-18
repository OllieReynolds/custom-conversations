import torch
import os

class Config:
    def __init__(self, **kwargs):
        self.model_directory = kwargs.get('model_directory', "../models/default")
        self.model_name = kwargs.get('model_name', "gpt2")
        self.file_path = kwargs.get('file_path', os.path.join(os.path.dirname(os.path.abspath(__file__)), '../input/default.txt'))
        self.device = kwargs.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')

        # General model settings
        self.model_type = kwargs.get('model_type', 'auto')  # 'gpt2', 'bert', 't5', 'auto' for automatic detection
        self.preprocessing_function_name = kwargs.get('preprocessing_function_name', 'default_preprocess')
        self.max_seq_length = kwargs.get('max_seq_length', 512)
        self.padding_strategy = kwargs.get('padding_strategy', 'max_length')
        self.truncation_strategy = kwargs.get('truncation_strategy', True)
        
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
        
        # Advanced Features
        self.use_early_stopping = kwargs.get('use_early_stopping', False)
        self.early_stopping_patience = kwargs.get('early_stopping_patience', 3)
        self.use_lr_scheduler = kwargs.get('use_lr_scheduler', True)
        self.lr_scheduler_type = kwargs.get('lr_scheduler_type', 'linear')

        # Model-specific Features
        self.model_features = kwargs.get('model_features', {})

        # Required files setup
        self.required_files = kwargs.get('required_files', ['config.json'])

    def to_dict(self):
        return self.__dict__
