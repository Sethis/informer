from typing import Optional
from abc import ABC, abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.dto import (
    UserRequestDTO,
    UserDTO,
    EncodedDataRequestDTO,
    EncodedDataDTO,
)
from src.adapters.database.structures import (
    User,
    EncodedData
)


class AbstractUserDAO(ABC):
    @abstractmethod
    async def get_user(
            self,
            user_id: Optional[int] = None,
            user_tg_id: Optional[int] = None
    ) -> Optional[UserDTO]:
        """
        User search by parameters
        :param user_id: Optional search parameter by User.id
        :param user_tg_id: Optional search parameter by User.tg_id
        :return: The user's object if it is found according to the
        parameters and nothing else in the opposite case
        """
        raise NotImplementedError()

    @abstractmethod
    async def insert_user(self, user: UserRequestDTO) -> UserDTO:
        """
        User's upset. Inserts a user using the user object
        or updating it in case of an identity conflict
        :param user: The object of the data
        that will be attached to the new user
        :return: The final user object
        """
        raise NotImplementedError()

    @abstractmethod
    async def insert_encoded_data(
            self,
            data: EncodedDataRequestDTO
    ) -> EncodedDataDTO:
        """
        Encoded data's insert. Inserts a encoded data using the data object
        :param data: The object of the data
        that will be attached to the new encoded data
        :return: The final encoded data object
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_encoded_data(
            self,
            data_id: int
    ) -> Optional[EncodedDataDTO]:
        """
        Encoded data's insert. Inserts a encoded data using the data object
        :param data_id: id of encoded data
        :return: The encoded data object if it is found by data_id
        and nothing else in the opposite case
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_encoded_data(self, data_id: int) -> bool:
        """
        Hides the encoded data by data_id
        :param data_id: id of encoded data
        :return: The value is True if the deletion was successful
        """
        raise NotImplementedError()


class SqlalchemyUserDAO(AbstractUserDAO):
    __slots__ = ("_session", )

    def __init__(self, session: AsyncSession, ):
        self._session = session

    async def get_user(
            self,
            user_id: Optional[int] = None,
            user_tg_id: Optional[int] = None
    ) -> Optional[UserDTO]:
        if not user_id and not user_tg_id:
            raise ValueError("One of the parameters must be passed.")

        stmt = select(User)

        if user_id:
            stmt = stmt.where(User.id == user_id)

        if user_tg_id:
            stmt = stmt.where(User.tg_id == user_tg_id)

        result = await self._session.scalar(stmt)

        if not result:
            return None

        return UserDTO.model_validate(result, from_attributes=True)

    async def insert_user(self, user: UserRequestDTO) -> UserDTO:
        stmt = (
            insert(User)
            .on_conflict_do_update(
                index_elements=["tg_id", ],
                set_={"is_admin": user.is_admin}
            )
            .values(**user.model_dump())
            .returning(User)
        )

        result = await self._session.scalar(stmt)

        return UserDTO.model_validate(result, from_attributes=True)


    async def insert_encoded_data(
            self,
            data: EncodedDataRequestDTO
    ) -> EncodedDataDTO:

        stmt = (
            insert(EncodedData)
            .values(**data.model_dump())
            .returning(EncodedData)
        )

        result = await self._session.scalar(stmt)

        return EncodedDataDTO.model_validate(result, from_attributes=True)

    async def get_encoded_data(
            self,
            data_id: int
    ) -> Optional[EncodedDataDTO]:
        stmt = select(EncodedData).where(EncodedData.id == data_id)

        result = await self._session.scalar(stmt)

        if not result:
            return None

        return EncodedDataDTO.model_validate(result, from_attributes=True)

    async def delete_encoded_data(self, data_id: int) -> bool:
        stmt = delete(EncodedData).where(EncodedData.id == data_id)

        await self._session.execute(stmt)

        return True
