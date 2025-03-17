from sqlalchemy.ext.asyncio import create_async_engine

from bot.config_data.config import load_config, Config

config: Config = load_config()

if config.postgres.debug:
    ENGINE = \
        f"sqlite+aiosqlite:///bot/database/{config.postgres.postgres_db}.db"
else:
    ENGINE = (
        f'postgresql+asyncpg://'
        f'{config.postgres.postgres_user}:'
        f'{config.postgres.postgres_password}'
        f'@postgres_db_container/{config.postgres.postgres_db}'
    )


def engine():
    return create_async_engine(ENGINE)
