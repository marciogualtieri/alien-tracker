from typing import Any

import numpy as np


class Shingle:
    """
    The input screen needs to be broken into shingles (small sliding view windows the size of the invader) that
    cover the whole screen. Named after the technique used in similarity detection: "shingling".
    """

    def __init__(self, contents: np.array, row: int, col: int, empty_value: Any):
        self.contents = contents
        self.empty_value = empty_value
        self.row_index_range = self._get_non_empty_row_index_range(row, empty_value)
        self.col_index_range = self._get_non_empty_col_index_range(col, empty_value)

    def _get_non_empty_row_index_range(self, row, empty_value):
        rows, _ = self.contents.shape
        non_empty_rows, _ = np.where(self.contents != empty_value)
        first_non_empty_row = non_empty_rows[0] - (rows - 1) + row
        last_non_empty_row = non_empty_rows[-1] - (rows - 1) + row
        return first_non_empty_row, last_non_empty_row + 1

    def _get_non_empty_col_index_range(self, column, empty_value):
        _, cols = self.contents.shape
        _, non_empty_cols = np.where(self.contents != empty_value)
        first_non_empty_col = non_empty_cols[0] - (cols - 1) + column
        last_non_empty_col = non_empty_cols[-1] - (cols - 1) + column
        return first_non_empty_col, last_non_empty_col + 1
