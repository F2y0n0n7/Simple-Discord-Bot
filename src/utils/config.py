import copy
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.json"

DEFAULT_CONFIG = {
    "status": {
        "enabled": True,
        "channel_id": None,
        "update_interval": 30,
        "embed_color": "0xFFADD8E6",
        "modules": {
            "uptime": True,
            "ping": True,
            "memory": True,
            "cpu": True,
            "disk": True,
            "network": True,
        }
    }
}


class ConfigError(Exception):
    """Raised when the config file is missing, unreadable or invalid."""


def setup_config():
    print("[Config] Setting up config...")
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
    except OSError as e:
        raise ConfigError(f"Could not write config file '{CONFIG_FILE}': {e}") from e
    print(f"[Config] Config file created: {CONFIG_FILE}")


def load_config():
    if not CONFIG_FILE.exists():
        raise ConfigError(f"Config file '{CONFIG_FILE}' does not exist.")
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError(
            f"Config file '{CONFIG_FILE}' is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}"
        ) from e
    except OSError as e:
        raise ConfigError(f"Could not read config file '{CONFIG_FILE}': {e}") from e
    if not isinstance(data, dict):
        raise ConfigError(f"Config file '{CONFIG_FILE}' must contain a JSON object at top level.")
    return data


def get_cog_config(cog_name):
    config = copy.deepcopy(DEFAULT_CONFIG.get(cog_name, {}))
    section = load_config().get(cog_name)
    if section is None:
        return config
    if not isinstance(section, dict):
        raise ConfigError(f"Section '{cog_name}' in '{CONFIG_FILE}' must be a JSON object.")
    config.update(section)
    return config
