from unittest import TestCase

import numpy as np

from alien_tracker.detectors import SimpleDetector
from alien_tracker.representations import TextRepresentation
from alien_tracker.shingle import Shingle


class TestDetectors(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_invader = TextRepresentation(
            """
                                       -o
                                       o-"""
        )

        cls.test_shingle_with_invader = Shingle(
            np.array([["-", "o"], ["o", "-"]]), 1, 1, "\0"
        )

        cls.empty_test_shingle = Shingle(
            np.array([["\0", "\0"], ["\0", "-"]]), 0, 0, "\0"
        )

        cls.test_shingle_with_noise = Shingle(
            np.array([["-", "o"], ["o", "o"]]), 1, 1, "\0"
        )

    def test_simple_detector_detected(self):
        test_detector = SimpleDetector(0.7)
        self.assertEqual(
            test_detector.score(self.test_invader, self.test_shingle_with_invader), 1.0
        )
        self.assertTrue(
            test_detector.detected(self.test_invader, self.test_shingle_with_invader)
        )

    def test_simple_detector_undetected(self):
        test_detector = SimpleDetector(0.7)
        self.assertEqual(
            test_detector.score(self.test_invader, self.empty_test_shingle), 0.25
        )
        self.assertFalse(
            test_detector.detected(self.test_invader, self.empty_test_shingle)
        )

    def test_simple_detector_detected_with_noise(self):
        test_detector = SimpleDetector(0.7)
        self.assertEqual(
            test_detector.score(self.test_invader, self.test_shingle_with_noise), 0.75
        )
        self.assertTrue(
            test_detector.detected(self.test_invader, self.test_shingle_with_noise)
        )
