from alembic.config import Config
from alembic import command
from pathlib import Path
from unnoti_corestore.utils.config_loader import Config as AppConfig

def run_migrations():
    if not AppConfig.DATABASE_URL:
        raise RuntimeError("DATABASE_URL missing; migrations aborted")

    repo_root = Path(__file__).resolve().parents[1]
    alembic_cfg = Config(str(repo_root / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", AppConfig.DATABASE_URL)
    alembic_cfg.set_main_option("script_location", str(repo_root / "unnoti_dbforge/migrations"))
    command.upgrade(alembic_cfg, "head")