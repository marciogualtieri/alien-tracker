from unittest import TestCase

import numpy as np
import numpy.testing as np_test

from alien_tracker.shingle import Shingle


class TestShingle(TestCase):

    def test_create_first_outside_screen_shingle(self):
        test_shingle_contents = np.array([["\0", "\0", "\0"],
                                          ["\0", "\0", "\0"],
                                          ["\0", "\0", "-"]])

        test_shingle = Shingle(test_shingle_contents, 0, 0, "\0")

        self.assertEqual(test_shingle.row_index_range, (0, 1))
        self.assertEqual(test_shingle.col_index_range, (0, 1))
        np_test.assert_array_equal(test_shingle.contents, test_shingle_contents)

    def test_create_next_outside_screen_shingle_to_the_left(self):
        test_shingle_contents = np.array([["\0", "\0", "\0"],
                                          ["\0", "\0", "\0"],
                                          ["\0", "-", "-"]])

        test_shingle = Shingle(test_shingle_contents, 0, 1, "\0")

        self.assertEqual(test_shingle.row_index_range, (0, 1))
        self.assertEqual(test_shingle.col_index_range, (0, 2))
        np_test.assert_array_equal(test_shingle.contents, test_shingle_contents)

    def test_create_next_outside_screen_shingle_down(self):
        test_shingle_contents = np.array([["\0", "\0", "\0"],
                                          ["\0", "-", "-"],
                                          ["\0", "-", "-"]])

        test_shingle = Shingle(test_shingle_contents, 1, 1, "\0")

        self.assertEqual(test_shingle.row_index_range, (0, 2))
        self.assertEqual(test_shingle.col_index_range, (0, 2))
        np_test.assert_array_equal(test_shingle.contents, test_shingle_contents)

    def test_create_first_inside_screen_shingle(self):
        test_shingle_contents = np.array([["-", "-", "-"],
                                          ["-", "-", "-"],
                                          ["-", "-", "-"]])

        test_shingle = Shingle(test_shingle_contents, 2, 2, "\0")

        self.assertEqual(test_shingle.row_index_range, (0, 3))
        self.assertEqual(test_shingle.col_index_range, (0, 3))
        np_test.assert_array_equal(test_shingle.contents, test_shingle_contents)

    def test_create_next_inside_screen_shingle_to_the_left(self):
        test_shingle_contents = np.array([["-", "-", "o"],
                                          ["-", "-", "o"],
                                          ["-", "-", "o"]])

        test_shingle = Shingle(test_shingle_contents, 2, 3, "\0")

        self.assertEqual(test_shingle.row_index_range, (0, 3))
        self.assertEqual(test_shingle.col_index_range, (1, 4))
        np_test.assert_array_equal(test_shingle.contents, test_shingle_contents)

    def test_create_next_inside_screen_shingle_down(self):
        test_shingle_contents = np.array([["-", "-", "o"],
                                          ["-", "-", "o"],
                                          ["o", "o", "o"]])

        test_shingle = Shingle(test_shingle_contents, 3, 3, "\0")

        self.assertEqual(test_shingle.row_index_range, (1, 4))
        self.assertEqual(test_shingle.col_index_range, (1, 4))
        np_test.assert_array_equal(test_shingle.contents, test_shingle_contents)
