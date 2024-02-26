from dataclasses import fields
import os
from typing import Optional
from config_definitions import Config
from dotenv import load_dotenv

load_dotenv()

def str_to_bool(value: str) -> bool:
    return value.lower() in ('true', '1', 't', 'y', 'yes')


def get_env_variable(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)

def load_config():
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
    return Config(**config_args) # type: ignore

app_config = load_config()

def main():
    config = load_config()

    print("Loaded Configuration:")
    print(f"File Path (str): {config.file_path}")
    print(f"Device (str): {config.device}")
    print(f"Num Train Epochs (int): {config.num_train_epochs}")
    print(f"Learning Rate (float): {config.learning_rate}")
    print(f"FP16 (bool): {config.fp16}")
    print(f"Model Features (Dict[str, str]): {config.model_features}")
    print(f"Required Files (List[str]): {config.required_files}")

    assert isinstance(config.file_path, str), "File Path is not of type str"
    assert isinstance(config.device, str), "Device is not of type str"
    assert isinstance(config.num_train_epochs, int), "Num Train Epochs is not of type int"
    assert isinstance(config.learning_rate, float), "Learning Rate is not of type float"
    assert isinstance(config.fp16, bool), "FP16 is not of type bool"
    assert isinstance(config.model_features, dict), "Model Features is not of type dict"
    assert isinstance(config.required_files, list), "Required Files is not of type list"

    assert config.file_path == "app/backend/input/sample.txt", f"File path incorrect. Expected 'app/backend/input/sample.txt', got '{config.file_path}'"
    assert config.device == "cpu", f"Device incorrect. Expected 'cpu', got '{config.device}'"
    assert config.num_train_epochs == 20, f"Num Train Epochs incorrect. Expected 20, got {config.num_train_epochs}"
    assert config.learning_rate == 0.00003, f"Learning Rate incorrect. Expected 0.00003, got {config.learning_rate}"
    assert config.fp16 is True, "FP16 should be True"
    assert config.model_features == {}, "Model Features should be an empty dict"
    assert config.required_files == ['config.json'], "Required Files should contain ['config.json']"

    print("Configuration loaded correctly from .env file and verified for each unique data type.")

if __name__ == "__main__":
    load_dotenv(dotenv_path='.env.test', override=True)
    main()

