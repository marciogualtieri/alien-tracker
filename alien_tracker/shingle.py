import numpy as np


class Shingle:

    def __init__(self, contents, row, col, empty_value):
        self.row_index_range = self.get_row_index_range(contents, row, empty_value)
        self.col_index_range = self.get_col_index_range(contents, col, empty_value)
        self.contents = contents
        self.empty_value = empty_value

    @staticmethod
    def get_row_index_range(contents, row, empty_value):
        rows, _ = contents.shape
        non_empty_rows, _ = np.where(contents != empty_value)
        first_non_empty_row = non_empty_rows[0] - (rows - 1) + row
        last_non_empty_row = non_empty_rows[-1] - (rows - 1) + row
        return first_non_empty_row, last_non_empty_row + 1

    @staticmethod
    def get_col_index_range(contents, column, empty_value):
        _, cols = contents.shape
        _, non_empty_cols = np.where(contents != empty_value)
        first_non_empty_col = non_empty_cols[0] - (cols - 1) + column
        last_non_empty_col = non_empty_cols[-1] - (cols - 1) + column
        return first_non_empty_col, last_non_empty_col + 1
