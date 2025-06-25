import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import models

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.settings import settings
from core.database import get_database_urls, Base

config = context.config
fileConfig(config.config_file_name)

database_url, _, test_database_url, _ = get_database_urls()

if settings.ENVIRONMENT == "production":
    sqlalchemy_url = database_url
else:
    sqlalchemy_url = test_database_url

config.set_main_option("sqlalchemy.url", sqlalchemy_url)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
