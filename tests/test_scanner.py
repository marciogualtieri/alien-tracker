from unittest import TestCase

import numpy as np
import numpy.testing as np_test

from alien_tracker.decoders import TextDecoder
from alien_tracker.detectors import SimpleDetector
from alien_tracker.tracker import Tracker


class TestScanner(TestCase):

    def test_extract_shingles(self):
        test_screen = TextDecoder("""
                                  abc
                                  def
                                  """)
        test_invaders = [TextDecoder("""
                                     ab
                                     de
                                     """),
                         TextDecoder("""
                                     bc
                                     ef
                                     """)
                         ]
        test_detector = SimpleDetector(0.9)
        scanner = Tracker(test_screen, test_invaders, test_detector, "\0")
        np_test.assert_array_equal(
            scanner.track_invaders(),
            [np.array([[True, True, False],
                       [True, True, False]]),
             np.array([[False, True, True],
                       [False, True, True]])])
