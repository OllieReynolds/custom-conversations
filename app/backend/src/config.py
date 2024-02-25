import os
import torch
from dataclasses import dataclass, field
from typing import Dict, List
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

def get_env_variable(key: str, default: str) -> str:
    return os.getenv(key, default)

@dataclass
class ModelConfig:
    model_directory: str = get_env_variable('MODEL_DIRECTORY', "../trained_model")
    model_name: str = get_env_variable('MODEL_NAME', "gpt2")
    model_type: str = get_env_variable('MODEL_TYPE', "auto")
    model_features: Dict[str, str] = field(default_factory=dict)

@dataclass
class TrainingConfig:
    num_train_epochs: int = int(get_env_variable('NUM_TRAIN_EPOCHS', "20"))
    per_device_train_batch_size: int = int(get_env_variable('PER_DEVICE_TRAIN_BATCH_SIZE', "16"))
    gradient_accumulation_steps: int = int(get_env_variable('GRADIENT_ACCUMULATION_STEPS', "1"))
    fp16: bool = get_env_variable('FP16', "True") == "True"
    learning_rate: float = float(get_env_variable('LEARNING_RATE', "3e-5"))
    warmup_steps: int = int(get_env_variable('WARMUP_STEPS', "1000"))
    save_steps: int = int(get_env_variable('SAVE_STEPS', "10000"))
    save_total_limit: int = int(get_env_variable('SAVE_TOTAL_LIMIT', "2"))
    evaluation_strategy: str = get_env_variable('EVALUATION_STRATEGY', "steps")
    eval_steps: int = int(get_env_variable('EVAL_STEPS', "1000"))
    use_early_stopping: bool = get_env_variable('USE_EARLY_STOPPING', "False") == "True"
    early_stopping_patience: int = int(get_env_variable('EARLY_STOPPING_PATIENCE', "3"))
    use_lr_scheduler: bool = get_env_variable('USE_LR_SCHEDULER', "True") == "True"
    lr_scheduler_type: str = get_env_variable('LR_SCHEDULER_TYPE', "linear")

@dataclass
class GenerationConfig:
    max_length_increment: int = int(get_env_variable('MAX_LENGTH_INCREMENT', "500"))
    do_sample: bool = get_env_variable('DO_SAMPLE', "True") == "True"
    top_k: int = int(get_env_variable('TOP_K', "50"))
    no_repeat_ngram_size: int = int(get_env_variable('NO_REPEAT_NGRAM_SIZE', "2"))
    temperature: float = float(get_env_variable('TEMPERATURE', "0.8"))
    top_p: float = float(get_env_variable('TOP_P', "0.92"))

@dataclass
class AppConfig:
    file_path: str = get_env_variable('FILE_PATH', "../input/sample.txt")
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    required_files: List[str] = field(default_factory=lambda: ['config.json'])

    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)

def load_config() -> AppConfig:
    return AppConfig()

def main():
    logger = get_logger('config_test')
    
    config = load_config()

    env_vars = {
        'MODEL_DIRECTORY': config.model.model_directory,
        'MODEL_NAME': config.model.model_name,
    }

    for var in env_vars:
        if var in os.environ:
            logger.info(f"{var} loaded from .env file: {os.getenv(var)}")
        else:
            logger.info(f"{var} using default value: {getattr(config.model, var.lower())}")

if __name__ == '__main__':
    main()
