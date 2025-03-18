from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class NatsDelayedConsumerConfig:
    subject: str
    stream: str
    durable_name: str


@dataclass
class PostgresConfig:
    debug: str
    postgres_db: str
    postgres_user: str
    postgres_password: str


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig
    postgres: PostgresConfig
    delayed_consumer: NatsDelayedConsumerConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('TOKEN')),
        nats=NatsConfig(servers=env.list('NATS_SERVERS')),
        postgres=PostgresConfig(
            debug=env.bool('DEBUG'),
            postgres_db=env.str('POSTGRES_DB'),
            postgres_user=env.str('POSTGRES_USER'),
            postgres_password=env.str('POSTGRES_PASSWORD'),
        ),
        delayed_consumer=NatsDelayedConsumerConfig(
            subject=env('NATS_DELAYED_CONSUMER_SUBJECT'),
            stream=env('NATS_DELAYED_CONSUMER_STREAM'),
            durable_name=env('NATS_DELAYED_CONSUMER_DURABLE_NAME')
        )
    )
