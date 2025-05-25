from typing import AsyncIterable

from aiogram.types import TelegramObject

from dishka import Provider, provide, Scope, from_context

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import Config
from src.adapters.database.dao import (
    AbstractUserDAO,
    SqlalchemyUserDAO,
    AbstactCommonDAO,
    SqlalchemyCommonDAO,
    AbstractInformationDAO,
    SqlalchemyInformationDAO
)
from src.adapters.database.services import UserService, InformationService
from src.adapters.encryption import AbstractCodeEncoder, CaesarCodeEncoder
from src.presentation.render import AbstractCodeRender, SimpleCodeRender


class AppProvider(Provider):
    scope = Scope.APP

    config_provider = from_context(provides=Config)

    @provide(scope=Scope.APP)
    async def config(self, config: Config) -> async_sessionmaker:
        engine = create_async_engine(
            config.db_url,
            pool_size=50,
            pool_timeout=15,
            pool_recycle=1500,
            pool_pre_ping=True,
            max_overflow=15,
            connect_args={
                "server_settings": {"jit": "off"}
            }
        )

        return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def new_connection(self, sessionmaker: async_sessionmaker) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def user_dao(self, session: AsyncSession) -> AbstractUserDAO:
        return SqlalchemyUserDAO(session=session)

    @provide(scope=Scope.REQUEST)
    async def information_dao(self, session: AsyncSession) -> AbstractInformationDAO:
        return SqlalchemyInformationDAO(session=session)

    @provide(scope=Scope.REQUEST)
    async def common_dao(self, session: AsyncSession) -> AbstactCommonDAO:
        return SqlalchemyCommonDAO(session=session)

    @provide(scope=Scope.REQUEST)
    async def encoder(self, config: Config) -> AbstractCodeEncoder:
        return CaesarCodeEncoder(offset=config.encoder_offset)

    @provide(scope=Scope.REQUEST)
    async def user_service(
            self,
            obj: TelegramObject,
            user_dao: AbstractUserDAO,
            common_dao: AbstactCommonDAO,
            encoder: AbstractCodeEncoder
    ) -> UserService:
        try:
            user_id = obj.from_user.id  # NOQA

        except AttributeError:
            user_id = -1

        return UserService(
            user_dao=user_dao,
            common_dao=common_dao,
            current_user_tg_id=user_id,
            code_encoder=encoder
        )

    @provide(scope=Scope.REQUEST)
    async def information_service(
            self,
            information_dao: AbstractInformationDAO,
            common_dao: AbstactCommonDAO,
    ) -> InformationService:
        return InformationService(
            common_dao=common_dao,
            information_dao=information_dao
        )

    @provide(scope=Scope.APP)
    async def code_render(self) -> AbstractCodeRender:
        return SimpleCodeRender()
