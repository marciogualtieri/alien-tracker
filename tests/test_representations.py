import numpy as np
import numpy.testing as np_test

from alien_tracker.representations import TextFileRepresentation
from .test_case_helper import TestCaseHelper


class TestRepresentations(TestCaseHelper):
    @classmethod
    def setUpClass(cls):
        cls.text_file_test_invader_full_path = cls.get_test_resource_full_path(
            "invaders", "simple.txt"
        )
        cls.test_invader_representation = np.array([["a", "b"], ["c", "d"]])

    def test_text_file_invader_representation(self):
        test_invader = TextFileRepresentation(self.text_file_test_invader_full_path)
        np_test.assert_array_equal(test_invader.value, self.test_invader_representation)
