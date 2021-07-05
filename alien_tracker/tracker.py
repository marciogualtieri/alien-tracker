import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from alien_tracker.shingle import Shingle


class Tracker:

    def __init__(self, screen, invaders, detector, empty_value):
        self.screen = screen
        self.invaders = invaders
        self.detector = detector
        self.empty_value = empty_value

    def _extract_shingles(self, invader):
        tracking_area = self._create_tracking_area(invader)
        views = np.squeeze(sliding_window_view(tracking_area, window_shape=invader.decode().shape))
        view_rows = views.shape[0]
        view_cols = views.shape[1]

        return [
            Shingle(views[row][col], row, col, self.empty_value)
            for row in range(0, view_rows)
            for col in range(0, view_cols)
        ]

    def _track_invader(self, invader):
        detections = np.full(self.screen.decode().shape, False)
        shingles = self._extract_shingles(invader)

        for shingle in shingles:
            if self.detector.detected(invader, shingle):
                self._mark_detection(detections, shingle)
        return detections

    @staticmethod
    def _mark_detection(detections, shingle):
        row_start, row_end = shingle.row_index_range
        col_start, col_end = shingle.col_index_range
        detections[row_start:row_end, col_start:col_end] = True

    def track_invaders(self):
        return [self._track_invader(invader) for invader in self.invaders]

    def _create_tracking_area(self, invader):
        rows, cols = invader.decode().shape
        return np.pad(self.screen.decode(),
                      ((rows - 1, rows - 1), (cols - 1, cols - 1)),
                      constant_values=(self.empty_value, self.empty_value))
