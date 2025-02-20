import os
import sys

from alembic import context
from database import Base, engine
from sqlalchemy import engine_from_config, pool

# Load database connection from the config file
config = context.config

# Set the database URL from your environment variables
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", ""))

# Target metadata (SQLAlchemy models)
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode (without connecting to DB)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode (with DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
