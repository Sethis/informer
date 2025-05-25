from typing import Optional
import random
import string
from abc import ABC, abstractmethod


class AbstractCodeEncoder(ABC):
    @abstractmethod
    def encode(self, payload: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_new_unencrypted_code(self, lenght: int = 8) -> str:
        raise NotImplementedError()


class CaesarCodeEncoder(AbstractCodeEncoder):
    # We will execute the Caesar cipher,
    # although we should have used more complex cryptographic variants.
    # 1) demo project
    # 2) generation is needed for small links
    # 3) the project uses id:pass verification,
    # which is already safe enough

    __slots__ = (
        "_alphabet",
        "_offset_alphabet",
    )

    def __init__(self, offset: int, alphabet: Optional[list[str]] = None):
        if not alphabet:
            alphabet = string.ascii_letters

        self._alphabet = alphabet
        alphabet_lenght = len(self._alphabet)

        letter_by_index = {
            index: value
            for index, value
            in enumerate(self._alphabet)
        }

        self._offset_alphabet: dict[str, str] = {}

        for index, char in letter_by_index.items():
            index += offset

            if index >= alphabet_lenght:
                index -= alphabet_lenght

            self._offset_alphabet[char] = letter_by_index[index]

    def encode(self, payload: str) -> str:
        result = ""

        for char in payload:
            result = f"{result}{self._offset_alphabet[char]}"

        return result

    def get_new_unencrypted_code(self, lenght: int = 8) -> str:
        result = [random.choice(self._alphabet) for _ in range(8)]

        return "".join(result)
