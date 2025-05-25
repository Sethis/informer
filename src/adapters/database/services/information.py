from typing import Optional

from ..dao.information import AbstractInformationDAO
from ..dao.common import AbstactCommonDAO
from src.adapters.database.dto import (
    InformationDTO,
    InformationRequestDTO
)



class InformationService:
    __slots__ = (
        "_common_dao",
        "_information_dao",
    )

    def __init__(
            self,
            information_dao: AbstractInformationDAO,
            common_dao: AbstactCommonDAO,
    ):

        self._information_dao = information_dao
        self._common_dao = common_dao

    async def insert_information(
            self,
            information: InformationRequestDTO
    ) -> InformationDTO:

        result = await self._information_dao.insert_information(information)
        await self._common_dao.commit()

        return result


    async def get_informations(self) -> list[InformationDTO]:
        return await self._information_dao.get_informations()

    async def get_information_by_id(
            self,
            information_id: int
    ) -> Optional[InformationDTO]:
        result = await self._information_dao.get_information_by_id(
            information_id
        )

        if not result:
            raise ValueError("Information with this id was not found.")

        return result

    async def delete_information(self, information_id: int) -> bool:
        result = await self._information_dao.delete_information(information_id)

        await self._common_dao.commit()

        return result
