from typing import List, Any

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from alien_tracker.detectors import Detector
from alien_tracker.representations import Representation
from alien_tracker.shingle import Shingle


class Tracker:
    """
    Computes detection masks that shows the spots in the screen where invaders were detected.
    """

    def __init__(self, screen: Representation, detector: Detector, empty_value: Any):
        self.screen = screen
        self.detector = detector
        self.empty_value = empty_value

    def get_detection_masks(self, invaders: List[Representation]) -> List[np.array]:
        return [self._get_invader_detection_mask(invader) for invader in invaders]

    def _extract_shingles(self, invader):
        tracking_area = self._create_padded_tracking_area(invader)
        views = np.squeeze(
            sliding_window_view(tracking_area, window_shape=invader.value.shape)
        )
        view_rows, view_cols = views.shape[0:2]

        return [
            Shingle(views[row][col], row, col, self.empty_value)
            for row in range(0, view_rows)
            for col in range(0, view_cols)
        ]

    def _get_invader_detection_mask(self, invader):
        assert invader < self.screen, "Input invader should fit the screen."

        detection_mask = self._create_empty_detection_mask()
        shingles = self._extract_shingles(invader)
        for shingle in shingles:
            if self.detector.detected(invader, shingle):
                self._update_detection_mask(detection_mask, shingle)
        return detection_mask

    def _create_empty_detection_mask(self):
        return np.full(self.screen.value.shape, False)

    @staticmethod
    def _update_detection_mask(detection_mask, shingle):
        row_start, row_end = shingle.row_index_range
        col_start, col_end = shingle.col_index_range
        detection_mask[row_start:row_end, col_start:col_end] = True

    def _create_padded_tracking_area(self, invader):
        rows, cols = invader.value.shape
        return np.pad(
            self.screen.value,
            ((rows - 1, rows - 1), (cols - 1, cols - 1)),
            constant_values=(self.empty_value, self.empty_value),
        )
