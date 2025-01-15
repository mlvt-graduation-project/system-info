import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.yaml")

with open(CONFIG_PATH, "r") as f:
    _config = yaml.safe_load(f)

# Extract the values for easy access
MONGO_URI = _config["database"]["mongo_uri"]
MONGO_DB_NAME = _config["database"]["mongo_db_name"]
POSTGRES_URI = _config["database"]["postgres_uri"]