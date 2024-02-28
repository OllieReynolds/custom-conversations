from dataclasses import asdict
from app.backend.src.utils.config import load_config
from app.backend.src.utils.database import Database
from typing import Dict, Any

class ConfigManager:
    _instance = None

    def __init__(self, db: Database):
        self.db = db
        self.config = load_config()
        self.load_or_initialize_db_config()

    @classmethod
    def instance(cls, db: Database | None = None):
        if cls._instance is None and db is not None:
            cls._instance = cls(db)
        return cls._instance

    def load_or_initialize_db_config(self):
        db_config = self.db.get_all_config_values()
        for key, value in db_config.items():
            setattr(self.config, key, value)
        self.config = self.db.load_or_initialize_db_config(self.config)

    def update_config(self, key: str, value: Any):
        self.db.set_config_value(key, value)
        setattr(self.config, key, value)

    def get_all_config_values(self) -> Dict[str, Any]:
        return asdict(self.config)

    def get_config(self):
        return self.config
