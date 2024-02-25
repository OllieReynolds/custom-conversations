from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Dict
import torch
from logger import get_logger
from dotenv import load_dotenv

load_dotenv()

class ModelConfig(BaseSettings):
    model_directory: str = Field(default="../trained_model", env='MODEL_DIRECTORY')
    model_name: str = Field(default="gpt2", env='MODEL_NAME')
    model_type: str = Field(default="auto", env='MODEL_TYPE')
    model_features: Dict[str, str] = Field(default_factory=dict, env='MODEL_FEATURES')

class TrainingConfig(BaseSettings):
    num_train_epochs: int = Field(default=20, env='NUM_TRAIN_EPOCHS')
    per_device_train_batch_size: int = Field(default=16, env='PER_DEVICE_TRAIN_BATCH_SIZE')
    gradient_accumulation_steps: int = Field(default=1, env='GRADIENT_ACCUMULATION_STEPS')
    fp16: bool = Field(default=True, env='FP16')
    learning_rate: float = Field(default=3e-5, env='LEARNING_RATE')
    warmup_steps: int = Field(default=1000, env='WARMUP_STEPS')
    save_steps: int = Field(default=10000, env='SAVE_STEPS')
    save_total_limit: int = Field(default=2, env='SAVE_TOTAL_LIMIT')
    evaluation_strategy: str = Field(default="steps", env='EVALUATION_STRATEGY')
    eval_steps: int = Field(default=1000, env='EVAL_STEPS')
    use_early_stopping: bool = Field(default=False, env='USE_EARLY_STOPPING')
    early_stopping_patience: int = Field(default=3, env='EARLY_STOPPING_PATIENCE')
    use_lr_scheduler: bool = Field(default=True, env='USE_LR_SCHEDULER')
    lr_scheduler_type: str = Field(default="linear", env='LR_SCHEDULER_TYPE')

class GenerationConfig(BaseSettings):
    max_length_increment: int = Field(default=500, env='MAX_LENGTH_INCREMENT')
    do_sample: bool = Field(default=True, env='DO_SAMPLE')
    top_k: int = Field(default=50, env='TOP_K')
    no_repeat_ngram_size: int = Field(default=2, env='NO_REPEAT_NGRAM_SIZE')
    temperature: float = Field(default=0.8, env='TEMPERATURE')
    top_p: float = Field(default=0.92, env='TOP_P')

class AppConfig(BaseSettings):
    file_path: str = Field(default="../input/sample.txt", env='FILE_PATH')
    device: str = Field(default="cuda" if torch.cuda.is_available() else "cpu", env='DEVICE')
    required_files: List[str] = Field(default=['config.json'], env='REQUIRED_FILES')

    model: ModelConfig = ModelConfig()
    training: TrainingConfig = TrainingConfig()
    generation: GenerationConfig = GenerationConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "forbid"

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

    logger.info("Logger is configured and working.")

if __name__ == '__main__':
    main()
