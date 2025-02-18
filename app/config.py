import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.yaml")

with open(CONFIG_PATH, "r") as f:
    _config = yaml.safe_load(f)

# Extract the values for easy access
MONGO_URI = _config["database"]["MONGO_URI"]
MONGO_DB_NAME = _config["database"]["MONGO_DB"]
POSTGRES_HOST = _config["database"]["POSTGRES_HOST"]
POSTGRES_DB = _config["database"]["POSTGRES_DB"]
POSTGRES_USER = _config["database"]["POSTGRES_USER"]
POSTGRES_PASSWORD = _config["database"]["POSTGRES_PASSWORD"]