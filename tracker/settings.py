from json import load, dump
from os import environ
from pathlib import Path
from sys import exit


DEFAULT_MONGO_CONFIG = {
    "username": None,
    "password": None,
    "host": None,
    "port": None,
    "database": "tracker",
    "srv_mode": False
}
TEST = environ.get("TRACKER_TEST", False)

MONGO_CONFIG = {}

if not TEST:
    config_dir = Path.home() / ".config" / "tracker"
    config_file = config_dir / "config.json"

    if config_file.is_file():
        with config_file.open() as fd:
            MONGO_CONFIG = load(fd)
    else:
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file.touch()
        with config_file.open(mode="w") as fd:
            dump(DEFAULT_MONGO_CONFIG, fd, indent=4)
            print(f"Tracker : Template configuration set at {config_file}")


for key, default in (
    ("TRACKER_MONGODB_USERNAME", None),
    ("TRACKER_MONGODB_PASSWORD", None),
    ("TRACKER_MONGODB_HOST",     None),
    ("TRACKER_MONGODB_PORT",     27017),
    ("TRACKER_MONGODB_DATABASE", "tracker"),
    ("TRACKER_MONGODB_SRV_MODE", False),
):
    short_key = key.replace("TRACKER_MONGODB_", "").lower()
    attr = environ.get(key, default)

    if attr is None and not MONGO_CONFIG.get(short_key):
        print(f"Tracker : {short_key} must be set")
        exit(1)

    if key == "TRACKER_MONGODB_SRV_MODE" and isinstance(attr, str):
        attr = attr.lower() in ("true", "1", "yes")

    MONGO_CONFIG[short_key] = attr

MONGO_DATABASE = MONGO_CONFIG.get("database")
