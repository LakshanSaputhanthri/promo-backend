from logging.config import fileConfig
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine

# -----------------------------
# Fix import path
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

# -----------------------------
# Imports
# -----------------------------
from app.config import settings
from app.database import Base
from app.models.promotions import Promotion

# -----------------------------
# Alembic config
# -----------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------
# Metadata
# -----------------------------
target_metadata = Base.metadata

# -----------------------------
# Sync DB URL (Alembic MUST be sync)
# -----------------------------
SYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql+asyncpg",
    "postgresql+psycopg2",
)

engine = create_engine(SYNC_DATABASE_URL)


def run_migrations_offline():
    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
