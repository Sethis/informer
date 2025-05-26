from typing import Optional

from ..dao.user import AbstractUserDAO
from ..dao.common import AbstactCommonDAO
from src.adapters.database.dto import (
    UserDTO,
    UserRequestDTO,
    EncodedDataRequestDTO,
    UnencryptedDataDTO
)
from src.adapters.encryption import AbstractCodeEncoder



class UserService:
    __slots__ = (
        "_common_dao",
        "_user_dao",
        "_current_user",
        "_current_user_tg_id",
        "_encoder"
    )

    def __init__(
            self,
            user_dao: AbstractUserDAO,
            common_dao: AbstactCommonDAO,
            current_user_tg_id: int,
            code_encoder: AbstractCodeEncoder
    ):

        self._user_dao = user_dao
        self._common_dao = common_dao
        self._current_user_tg_id = current_user_tg_id
        self._current_user: Optional[UserDTO] = None
        self._encoder = code_encoder

    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        """
        This method does unsafe retrieve the user by user_Id.
        If the user is not found, it returns None
        :param user_id: User.id
        :return: UserDTO or None
        """

        return await self._user_dao.get_user(
            user_id=user_id
        )

    async def get_user_by_tg_id(self, user_tg_id: int) -> Optional[UserDTO]:
        """
        This method does unsafe retrieve the user by user_tg_id.
        If the user is not found, it returns None
        :param user_tg_id: User.Tg_id
        :return: UserDTO or None
        """

        return await self._user_dao.get_user(
            user_tg_id=user_tg_id
        )

    async def get_current_user(self) -> UserDTO:
        """
        This method safely retrieves the user by user_tg_id
        and caches the result for current session di scope
        :return: UserDTO or ValueError if user undefined
        """

        if self._current_user:
            return self._current_user

        user = await self.get_user_by_tg_id(self._current_user_tg_id)

        if not user:
            raise ValueError(
                "The user has not been found. "
                "The get_current_user is a safe method to get user, "
                "if the user can be None please use get_user_by_tg_id"
            )

        self._current_user = user

        return user

    async def insert_user(self, user: UserRequestDTO) -> UserDTO:
        """
        User's upsert. Inserts a user using the user object
        or updating it in case of an identity conflict
        :param user: The object of the data
        that will be attached to the new user
        :return: The final user object
        """

        result = await self._user_dao.insert_user(
            user=user
        )

        await self._common_dao.commit()

        return result

    async def check_admin_code(
            self,
            code_id: int,
            unenctypted_code: str
    ) -> bool:
        """
        Checks the code for existence and for compliance after encoding.
        Hides the code after that
        :param code_id: Encoded data id
        :param unenctypted_code: Unenctypted payload.
        The method encodes it itself
        :return: True if all operations are completed successfully,
        and false in the other case.
        """

        result = await self._user_dao.get_encoded_data(data_id=code_id)

        if not result:
            return False

        if self._encoder.encode(unenctypted_code) != result.payload:
            return False

        if not await self._user_dao.delete_encoded_data(code_id):
            return False

        await self._common_dao.commit()

        return True

    async def get_admin_code(self) -> UnencryptedDataDTO:
        code = self._encoder.get_new_unencrypted_code()
        encoded = self._encoder.encode(code)

        result = await self._user_dao.insert_encoded_data(
            EncodedDataRequestDTO(
                payload=encoded
            )
        )

        await self._common_dao.commit()

        return UnencryptedDataDTO(
            id=result.id,
            payload=code
        )
