from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class AbstactCommonDAO(ABC):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class SqlalchemyCommonDAO(AbstactCommonDAO):
    __slots__ = ("_session", )

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.commit()
