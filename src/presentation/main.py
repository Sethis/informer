import asyncio
import orjson

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs

from redis.asyncio import Redis

from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from src.presentation.providers import AppProvider
from src.config import reader, Config

from src.presentation.routers.common import common_router


async def main():
    config = reader()

    redis = Redis(
        host=config.redis_host,
        password=config.redis_password,
        port=config.redis_port,
        db=config.redis_db
    )
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(with_destiny=True),
        json_loads=orjson.loads,
        json_dumps=orjson.dumps  # noqa: ignore
    )

    container = make_async_container(
        AppProvider(),
        AiogramProvider(),
        context={Config: config}
    )

    bot = Bot(
        token=config.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    isolation = storage.create_isolation()

    dp = Dispatcher(events_isolation=isolation, storage=storage)

    dp.include_router(common_router)

    setup_dialogs(dp, events_isolation=isolation)
    setup_dishka(container=container, router=dp, auto_inject=True)

    dp.shutdown.register(container.close)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )

    finally:
        await container.close()
        await bot.session.close()


asyncio.run(main())
