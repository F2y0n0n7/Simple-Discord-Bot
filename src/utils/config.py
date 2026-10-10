import copy
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.json"

ALWAYS_ADD = {
    "bot_prefix": "!"
}

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


def _write_config(data):
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        raise ConfigError(f"Could not write config file '{CONFIG_FILE}': {e}") from e


def setup_config():
    """Creates the config file with the ALWAYS_ADD keys first, followed by the cog defaults."""
    print("[Config] Setting up config...")
    _write_config({**copy.deepcopy(ALWAYS_ADD), **copy.deepcopy(DEFAULT_CONFIG)})
    print(f"[Config] Config file created: {CONFIG_FILE}")


def ensure_config():
    """Creates the config if missing and adds missing ALWAYS_ADD keys at the top of an existing one."""
    if not CONFIG_FILE.exists():
        setup_config()
        return
    data = load_config()
    missing = {k: v for k, v in ALWAYS_ADD.items() if k not in data}
    if not missing:
        return
    rest = {k: v for k, v in data.items() if k not in ALWAYS_ADD}
    present = {k: data[k] for k in ALWAYS_ADD if k in data}
    _write_config({**present, **copy.deepcopy(missing), **rest})
    print(f"[Config] Added missing keys to config: {', '.join(missing)}")


def get_value(key):
    """Returns a top-level config value, falling back to its ALWAYS_ADD default."""
    return load_config().get(key, ALWAYS_ADD.get(key))

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
