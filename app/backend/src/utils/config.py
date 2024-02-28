from dataclasses import dataclass, field, asdict, fields
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

@dataclass
class Config:
    file_path: str = "app/backend/input/sample.txt"
    device: str = "cuda"
    model_directory: str = "app/backend/trained_model"
    model_name: str = "gpt2"
    model_type: str = "auto"
    model_features: Dict[str, str] = field(default_factory=dict)
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
    max_length_increment: int = 500
    do_sample: bool = True
    top_k: int = 50
    no_repeat_ngram_size: int = 2
    temperature: float = 0.9
    top_p: float = 0.92

class ConfigManager:
    _instance = None

    def __init__(self, db: Any):
        self.db = db
        self.config = load_config()
        self.load_or_initialize_db_config()

    @classmethod
    def instance(cls, db: Any | None = None):
        if cls._instance is None and db is not None:
            cls._instance = cls(db)
        return cls._instance

    def load_or_initialize_db_config(self):
        db_config = self.db.get_all_config_values()
        config_fields = {field.name: field.type for field in fields(Config)}
        for key, value in db_config.items():
            if key in config_fields:
                casted_value = self.db.convert_value(config_fields[key], value)
                setattr(self.config, key, casted_value)

    def update_config(self, key: str, value: Any):
        self.db.set_config_value(key, value)
        setattr(self.config, key, value)

    def get_all_config_values(self) -> Dict[str, Any]:
        return asdict(self.config)

    def get_config(self):
        return self.config

def str_to_bool(value: str) -> bool:
    return value.lower() in ('true', '1', 't', 'y', 'yes')

def get_env_variable(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)

def load_config() -> Config:
    temp_config = Config()
    config_args = {}
    for field in fields(Config):
        field_value = get_env_variable(field.name.upper(), getattr(temp_config, field.name))
        if field.type == bool:
            config_args[field.name] = str_to_bool(field_value) if field_value is not None else False
        elif field.type == int:
            config_args[field.name] = int(field_value) if field_value and field_value.isdigit() else getattr(temp_config, field.name)
        elif field.type == float:
            try:
                config_args[field.name] = float(field_value) if field_value is not None else getattr(temp_config, field.name)
            except ValueError:
                config_args[field.name] = getattr(temp_config, field.name)
        else:
            config_args[field.name] = field_value
    return Config(**config_args)

app_config = load_config()

def main():
    load_dotenv(dotenv_path='.env.test', override=True)
    config = load_config()

    print("Loaded Configuration:")
    print(f"File Path: {config.file_path}")
    print(f"Device: {config.device}")
    print(f"Num Train Epochs: {config.num_train_epochs}")
    print(f"Learning Rate: {config.learning_rate}")
    print(f"FP16: {config.fp16}")
    print(f"Model Features: {config.model_features}")

if __name__ == "__main__":
    main()
