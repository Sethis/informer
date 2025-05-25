from typing import Optional
from abc import ABC, abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.dto import (
    InformationRequestDTO,
    InformationDTO
)
from src.adapters.database.structures import (
    Information,
)


class AbstractInformationDAO(ABC):
    @abstractmethod
    async def insert_information(
            self,
            information: InformationRequestDTO
    ) -> InformationDTO:
        """
        Informations blocks insert using the information object
        :param information: The object of the data
        that will be attached to the new information
        :return: The final information data object
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_informations(self) -> list[InformationDTO]:
        """
        Search and return of all information objects
        :return: array of information blocks for the entire application
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_information_by_id(
            self,
            information_id: int
    ) -> Optional[InformationDTO]:
        """
        Search and return of one information objects by id
        :param information_id: information id for search
        :return: one information objects by id
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_information(self, information_id: int) -> bool:
        """
        Hides the information by information_id
        :param information_id: id of the information to be deleted
        :return: The value is True if the deletion was successful
        """
        raise NotImplementedError()


class SqlalchemyInformationDAO(AbstractInformationDAO):
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession, ):
        self._session = session

    async def insert_information(
            self,
            information: InformationRequestDTO
    ) -> InformationDTO:

        stmt = (
            insert(Information)
            .values(**information.model_dump())
            .returning(Information)
        )

        result = await self._session.scalar(stmt)

        return InformationDTO.model_validate(result, from_attributes=True)

    async def get_informations(self) -> list[InformationDTO]:
        stmt = select(Information).order_by(Information.id.asc())

        result = await self._session.scalars(stmt)

        return [
            InformationDTO.model_validate(value, from_attributes=True)
            for value in result
        ]

    async def get_information_by_id(
            self,
            information_id: int
    ) -> Optional[InformationDTO]:
        stmt = select(Information).where(Information.id == information_id)

        result = await self._session.scalar(stmt)

        if not result:
            return None

        return InformationDTO.model_validate(result, from_attributes=True)

    async def delete_information(self, information_id: int) -> bool:
        stmt = delete(Information).where(Information.id == information_id)

        await self._session.execute(stmt)

        return True
