import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.config_data.config import load_config
from bot.database.engine import engine
from bot.handlers import all_router
from bot.middlewares.i18n import TranslatorRunnerMiddleware
from bot.middlewares.session import DbSessionMiddleware
from bot.middlewares.track_all_users import TrackAllUsersMiddleware
from bot.config_data import Config
from bot.service.i18n import create_translator_hub
from bot.service.nats_connect import connect_to_nats
from bot.service.nats_storage import NatsStorage

logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(filename)s:%(lineno)d "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


async def start_bot():

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Подключаемся к NATS
    nc, js = await connect_to_nats(servers=config.nats.servers)

    # Инициализируем хранилище на базе NATS
    storage: NatsStorage = await NatsStorage(nc=nc, js=js).create_storage()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)
    dp.include_router(all_router)

    sessionmaker = async_sessionmaker(engine(), expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    translator_hub: TranslatorHub = create_translator_hub()
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.errors.middleware(TranslatorRunnerMiddleware())

    try:
        await dp.start_polling(bot, _translator_hub=translator_hub)
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем соединение с NATS
        await nc.close()
        logger.info('Connection to NATS closed')
