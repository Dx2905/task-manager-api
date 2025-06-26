from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Import your app modules (add root to sys.path)
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

# Import Base and all models
from app.core.database import Base
from app import models  # Assumes __init__.py inside models/
  # include more models as you add them

# Alembic config
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic what metadata to autogenerate from
target_metadata = Base.metadata

# --- Offline migration mode ---
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# --- Online migration mode ---
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # optional: helps detect column type changes
        )

        with context.begin_transaction():
            context.run_migrations()

# Entry point
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
