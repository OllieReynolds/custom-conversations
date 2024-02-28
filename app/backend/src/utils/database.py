import sqlite3
from typing import Any, Dict, Optional, Type
from dataclasses import fields

from app.backend.src.utils.config_definitions import Config
from app.backend.src.utils.logger import get_logger

import json
from dataclasses import fields
from typing import Any, Dict, Type

class Database:
    DATABASE = 'config.db'

    def __init__(self):
        self.logger = get_logger(__name__)
        self.init_db()

    def init_db(self) -> None:
        try:
            conn = sqlite3.connect(self.DATABASE)
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')
            conn.commit()
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
        finally:
            conn.close()
            self.logger.info("Database initialized or checked successfully")
            
    def str_to_bool(self, value: str) -> bool:
        return value.lower() in ('true', '1', 't', 'y', 'yes')
            
    def convert_value(self, type_hint: Type, value: str) -> Any:
        if type_hint == bool:
            return self.str_to_bool(value)
        elif type_hint == int:
            return int(value)
        elif type_hint == float:
            return float(value)
        elif type_hint == Dict[str, str]:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return {}
        else:
            return value

    def get_db_connection(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.DATABASE)
            conn.row_factory = sqlite3.Row
            self.logger.info("Database connection established")
            return conn
        except Exception as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise e

    def get_all_config_values(self) -> Dict[str, Optional[str]]:
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            c.execute('SELECT key, value FROM config')
            all_values = c.fetchall()
            self.logger.info("Retrieved all config values")
            return {row['key']: row['value'] for row in all_values}
        except Exception as e:
            self.logger.error(f"Error retrieving all config values: {e}")
        finally:
            conn.close()
        return {}

    def get_config_value(self, key: str) -> Optional[str]:
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            c.execute('SELECT value FROM config WHERE key = ?', (key,))
            value = c.fetchone()
            self.logger.info(f"Retrieved config value for key: {key}")
            return value['value'] if value else None
        except Exception as e:
            self.logger.error(f"Error retrieving config value for key: {key}, Error: {e}")
        finally:
            conn.close()

    def set_config_value(self, key: str, value: str) -> None:
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO config (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?', (key, value, value))
            conn.commit()
            self.logger.info(f"Set config value for key: {key}")
        except Exception as e:
            self.logger.error(f"Error setting config value for key: {key}, Error: {e}")
        finally:
            conn.close()

    def load_or_initialize_db_config(self, config: Config) -> Config:
        conn = self.get_db_connection()
        c = conn.cursor()

        for field in fields(Config):
            key = field.name
            default_value = getattr(config, key)
            c.execute('INSERT INTO config (key, value) VALUES (?, ?) ON CONFLICT(key) DO NOTHING', (key, str(default_value)))

        conn.commit()

        c.execute('SELECT key, value FROM config')
        all_values = c.fetchall()
        config_fields = {field.name: field.type for field in fields(Config)}
        for row in all_values:
            key, value = row['key'], row['value']
            if key in config_fields:
                casted_value = self.convert_value(config_fields[key], value)
                setattr(config, key, casted_value)

        conn.close()
        return config
