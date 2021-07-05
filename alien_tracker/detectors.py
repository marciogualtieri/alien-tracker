from abc import ABC
from abc import abstractmethod

import numpy as np


class Detector(ABC):
    def detected(self, invader, shingle):
        return self.score(invader, shingle) > self.threshold

    @abstractmethod
    def score(self, invader, shingle):
        pass


class SimpleDetector(Detector):

    def __init__(self, threshold):
        assert 0 < threshold < 1
        self.threshold = threshold

    def score(self, invader, shingle):
        return np.mean(shingle.contents == invader.decode())
