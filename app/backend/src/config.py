from pydantic import BaseSettings, Field
from typing import List
import torch
from logger import get_logger
import os
from dotenv import load_dotenv

load_dotenv()

class ModelConfig(BaseSettings):
    model_directory: str = Field("../trained_model", env='MODEL_DIRECTORY')
    model_name: str = Field("gpt2", env='MODEL_NAME')
    model_type: str = Field("auto", env='MODEL_TYPE')
    model_features: dict = Field({}, env='MODEL_FEATURES')

class TrainingConfig(BaseSettings):
    num_train_epochs: int = Field(20, env='NUM_TRAIN_EPOCHS')
    per_device_train_batch_size: int = Field(16, env='PER_DEVICE_TRAIN_BATCH_SIZE')
    gradient_accumulation_steps: int = Field(1, env='GRADIENT_ACCUMULATION_STEPS')
    fp16: bool = Field(True, env='FP16')
    learning_rate: float = Field(3e-5, env='LEARNING_RATE')
    warmup_steps: int = Field(1000, env='WARMUP_STEPS')
    save_steps: int = Field(10000, env='SAVE_STEPS')
    save_total_limit: int = Field(2, env='SAVE_TOTAL_LIMIT')
    evaluation_strategy: str = Field("steps", env='EVALUATION_STRATEGY')
    eval_steps: int = Field(1000, env='EVAL_STEPS')
    use_early_stopping: bool = Field(False, env='USE_EARLY_STOPPING')
    early_stopping_patience: int = Field(3, env='EARLY_STOPPING_PATIENCE')
    use_lr_scheduler: bool = Field(True, env='USE_LR_SCHEDULER')
    lr_scheduler_type: str = Field("linear", env='LR_SCHEDULER_TYPE')

class GenerationConfig(BaseSettings):
    max_length_increment: int = Field(500, env='MAX_LENGTH_INCREMENT')
    do_sample: bool = Field(True, env='DO_SAMPLE')
    top_k: int = Field(50, env='TOP_K')
    no_repeat_ngram_size: int = Field(2, env='NO_REPEAT_NGRAM_SIZE')
    temperature: float = Field(0.8, env='TEMPERATURE')
    top_p: float = Field(0.92, env='TOP_P')

class AppConfig(BaseSettings):
    file_path: str = Field("../input/sample.txt", env='FILE_PATH')
    device: str = Field("cuda" if torch.cuda.is_available() else "cpu", env='DEVICE')
    required_files: List[str] = Field(['config.json'], env='REQUIRED_FILES')

    model: ModelConfig = ModelConfig()
    training: TrainingConfig = TrainingConfig()
    generation: GenerationConfig = GenerationConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

def load_config() -> AppConfig:
    return AppConfig()

config = load_config()

def main():    
    logger = get_logger('config_test')

    env_vars = {
        'MODEL_DIRECTORY': config.model.model_directory,
        'MODEL_NAME': config.model.model_name,
    }

    for var in env_vars:
        if var in os.environ:
            logger.info(f"{var} loaded from .env file: {os.getenv(var)}")
        else:
            logger.info(f"{var} using default value: {getattr(config.model, var.lower())}")

    logger.info("Logger is configured and working.")

if __name__ == '__main__':
    main()
