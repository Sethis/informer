from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(slots=True, kw_only=True)
class CodeData:
    code_id: int
    unencrypted_payload: str


class AbstractCodeRender(ABC):
    @abstractmethod
    def encode(self, code: CodeData) -> str:
        raise NotImplementedError()

    @abstractmethod
    def decode(self, code: str) -> CodeData:
        raise NotImplementedError()


class SimpleCodeRender(AbstractCodeRender):
    __slots__ = ("_separator", )

    def __init__(self, separator: str = "_"):
        self._separator = separator

    def encode(self, code: CodeData) -> str:
        return f"{code.code_id}{self._separator}{code.unencrypted_payload}"

    def decode(self, code: str) -> CodeData:
        splitted = code.split(self._separator)

        if len(splitted) != 2:
            raise ValueError(
                f"It was required to get 2 results"
                f" after splitting but {len(splitted)} were given"
            )

        return CodeData(
            code_id=int(splitted[0]),
            unencrypted_payload=splitted[1]
        )
