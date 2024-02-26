from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Config:
    # General App Config
    file_path: str = "app/backend/input/sample.txt"
    device: str = "cuda"
    required_files: List[str] = field(default_factory=lambda: ['config.json'])

    # Model Config
    model_directory: str = "app/backend/trained_model"
    model_name: str = "gpt2"
    model_type: str = "auto"
    model_features: Dict[str, str] = field(default_factory=dict)

    # Training Config
    num_train_epochs: int = 20
    per_device_train_batch_size: int = 16
    gradient_accumulation_steps: int = 1
    fp16: bool = True
    learning_rate: float = 0.00003
    warmup_steps: int = 1000
    save_steps: int = 10000
    save_total_limit: int = 2
    evaluation_strategy: str = "steps"
    eval_steps: int = 1000
    use_early_stopping: bool = False
    early_stopping_patience: int = 3
    use_lr_scheduler: bool = True
    lr_scheduler_type: str = "linear"
    logging_dir: str = "logs"
    logging_steps: int = 500
    do_train: bool = True
    do_eval: bool = True
    do_predict: bool = False
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "loss"
    greater_is_better: bool = False

    # Generation Config
    max_length_increment: int = 500
    do_sample: bool = True
    top_k: int = 50
    no_repeat_ngram_size: int = 2
    temperature: float = 0.9
    top_p: float = 0.92
