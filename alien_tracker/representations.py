from abc import ABC
from abc import abstractmethod

import numpy as np


class Representation(ABC):
    @property
    @abstractmethod
    def value(self) -> np.array:
        pass

    def __lt__(self, other):
        return self.value.shape < other.value.shape


class TextRepresentation(Representation):
    def __init__(self, text: str):
        self.text = self._remove_indentation(text)
        self.text_representation = np.array(
            [np.array(list(line), dtype="object") for line in self.text.splitlines()],
            dtype="object",
        )

    @property
    def value(self) -> np.array:
        return self.text_representation

    @staticmethod
    def _remove_indentation(text: str) -> str:
        return text.replace(" ", "").strip()


class TextFileRepresentation(TextRepresentation):
    def __init__(self, file_path: str):
        with open(file_path, "r") as f:
            text = f.read()
            super(TextFileRepresentation, self).__init__(text)
