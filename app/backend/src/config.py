from pydantic import BaseSettings, Field
from typing import List
import torch
from logger import get_logger
import os

class ModelConfig(BaseSettings):
    model_directory: str = Field("../models/default", env='MODEL_DIRECTORY')
    model_name: str = Field("gpt2", env='MODEL_NAME')
    model_type: str = Field("auto", env='MODEL_TYPE')
    model_features: dict = {}

class TrainingConfig(BaseSettings):
    num_train_epochs: int = 20
    per_device_train_batch_size: int = 16
    gradient_accumulation_steps: int = 1
    fp16: bool = True
    learning_rate: float = 3e-5
    warmup_steps: int = 1000
    save_steps: int = 10000
    save_total_limit: int = 2
    evaluation_strategy: str = "steps"
    eval_steps: int = 1000
    use_early_stopping: bool = False
    early_stopping_patience: int = 3
    use_lr_scheduler: bool = True
    lr_scheduler_type: str = "linear"

class GenerationConfig(BaseSettings):
    max_length_increment: int = 500
    do_sample: bool = True
    top_k: int = 50
    no_repeat_ngram_size: int = 2
    temperature: float = 0.8
    top_p: float = 0.92

class AppConfig(BaseSettings):
    file_path: str = "../input/default.txt"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    required_files: List[str] = ['config.json']

    model: ModelConfig = ModelConfig()
    training: TrainingConfig = TrainingConfig()
    generation: GenerationConfig = GenerationConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

def load_config() -> AppConfig:
    config = AppConfig()
    return config

config = load_config()

def main():
    logger = get_logger('config_test')

    config = load_config()

    env_vars = {
        'MODEL_DIRECTORY': config.model.model_directory,
        'MODEL_NAME': config.model.model_name,
    }

    for var, value in env_vars.items():
        default_value = ModelConfig.__fields__[var.lower()].default
        if os.getenv(var) == value:
            logger.info(f"{var} loaded from .env file: {value}")
        elif value == default_value:
            logger.info(f"{var} using default value: {value}")
        else:
            logger.info(f"{var} set explicitly (neither default nor from .env): {value}")
    logger.info("Logger is configured and working.")

if __name__ == '__main__':
    main()
