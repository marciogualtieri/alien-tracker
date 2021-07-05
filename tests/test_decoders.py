import numpy as np
import numpy.testing as np_test

from alien_tracker.decoders import TextFileDecoder
from .test_case_helper import TestCaseHelper


class TestDecoders(TestCaseHelper):

    @classmethod
    def setUpClass(cls):
        cls.text_file_test_invader_full_path = cls.get_test_resource_full_path("invaders", "simple.txt")
        cls.decoded_test_invader = np.array([["a", "b"], ["c", "d"]])

    def test_decode_text_file_invader(self):
        test_invader = TextFileDecoder(self.text_file_test_invader_full_path)
        np_test.assert_array_equal(
            test_invader.decode(),
            self.decoded_test_invader
        )
