import os
from pathlib import Path
from dotenv import load_dotenv

def find_env_file():
    env_override = os.getenv("ENV_PATH")
    if env_override and Path(env_override).exists():
        return Path(env_override)

    cwd = Path.cwd()
    for p in [cwd] + list(cwd.parents):
        candidate = p / ".env"
        if candidate.exists():
            return candidate

    here = Path(__file__).resolve()
    for p in here.parents:
        candidate = p / ".env"
        if candidate.exists():
            return candidate
    return None

env_file = find_env_file()
if env_file:
    load_dotenv(dotenv_path=env_file, override=False)
else:
    print("⚠️ No .env found; relying on environment variables")

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASEURL")
    APP_ENV = os.getenv("APP_ENV", "dev")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")