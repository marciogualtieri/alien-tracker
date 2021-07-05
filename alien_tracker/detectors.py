from abc import ABC
from abc import abstractmethod

import numpy as np

from alien_tracker.representations import Representation
from alien_tracker.shingle import Shingle


class Detector(ABC):
    def detected(self, invader: Representation, shingle: Shingle):
        return self.score(invader, shingle) > self.threshold

    @abstractmethod
    def score(self, invader, shingle) -> float:
        pass


class SimpleDetector(Detector):
    def __init__(self, threshold):
        assert 0 < threshold < 1
        self.threshold = threshold

    def score(self, invader: Representation, shingle: Shingle) -> float:
        return np.mean(shingle.contents == invader.value)
