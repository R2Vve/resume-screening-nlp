import os
from typing import Dict, Any
import yaml

class Config:
    def __init__(self, config_path: str = "config.yml"):
        self.config_path = config_path
        self.defaults = {
            "scoring_weights": {
                "similarity_score": 0.3,
                "skill_match": 0.3,
                "experience": 0.2,
                "education": 0.2
            },
            "minimum_score": 0.6,
            "preferred_formats": ["pdf", "docx", "txt"],
            "spacy_model": "en_core_web_sm",
            "sentence_transformer_model": "all-MiniLM-L6-v2",
            "database": {
                "path": "resume_screening.db"
            },
            "api": {
                "enable_rest_api": False,
                "port": 5000,
                "host": "127.0.0.1"
            }
        }
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create with defaults."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                return self._merge_configs(self.defaults, user_config)
        else:
            self._save_config(self.defaults)
            return self.defaults

    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def _merge_configs(self, default: Dict[str, Any], 
                      user: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge user config with defaults."""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        try:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def update(self, key: str, value: Any):
        """Update a configuration value."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self._save_config(self.config)
