from pydantic import BaseModel


class UserRequestDTO(BaseModel):
    tg_id: int
    is_admin: bool


class UserDTO(UserRequestDTO):
    id: int


class InformationRequestDTO(BaseModel):
    name: str
    text: str


class InformationDTO(InformationRequestDTO):
    id: int


class EncodedDataRequestDTO(BaseModel):
    payload: str


class EncodedDataDTO(EncodedDataRequestDTO):
    id: int

class UnencryptedDataDTO(BaseModel):
    id: int
    payload: str
