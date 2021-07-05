from unittest import TestCase

import numpy as np
import numpy.testing as np_test

from alien_tracker.detectors import SimpleDetector
from alien_tracker.representations import TextRepresentation
from alien_tracker.tracker import Tracker


class TestTracker(TestCase):
    def test_get_detections(self):
        test_screen = TextRepresentation(
            """
                                  abc
                                  def
                                  """
        )
        test_invaders = [
            TextRepresentation(
                """
                                     ab
                                     de
                                     """
            ),
            TextRepresentation(
                """
                                     bc
                                     ef
                                     """
            ),
        ]
        test_detector = SimpleDetector(0.9)
        scanner = Tracker(test_screen, test_detector, "\0")
        np_test.assert_array_equal(
            scanner.get_detection_masks(test_invaders),
            [
                np.array([[True, True, False], [True, True, False]]),
                np.array([[False, True, True], [False, True, True]]),
            ],
        )

    def test_invader_larger_than_screen(self):
        test_screen = TextRepresentation(
            """
                                  ab
                                  cd
                                  """
        )
        test_invaders = [
            TextRepresentation(
                """
                                  abc
                                  def
                                  ghi
                                     """
            ),
        ]
        test_detector = SimpleDetector(0.9)
        scanner = Tracker(test_screen, test_detector, "\0")

        with self.assertRaises(AssertionError) as context:
            scanner.get_detection_masks(test_invaders)

        self.assertIn("Input invader should fit the screen", str(context.exception))
