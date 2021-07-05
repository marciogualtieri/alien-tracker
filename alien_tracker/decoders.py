from abc import ABC
from abc import abstractmethod

import numpy as np


class Decoder(ABC):
    @abstractmethod
    def decode(self) -> np.array:
        pass


class TextDecoder(Decoder):

    def __init__(self, text):
        self.text = self._remove_indentation(text)

    def decode(self) -> np.array:
        return np.array([np.array(list(line), dtype="object") for line in self.text.splitlines()], dtype="object")

    @staticmethod
    def _remove_indentation(text) -> str:
        return text.replace(" ", "").strip()


class TextFileDecoder(TextDecoder):

    def __init__(self, file_path: str):
        with open(file_path, "r") as f:
            text = f.read()
            super(TextFileDecoder, self).__init__(text)
