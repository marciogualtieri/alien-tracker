from typing import List

from alien_tracker.detectors import SimpleDetector
from alien_tracker.renderers import StandardOutputRenderer
from alien_tracker.representations import TextFileRepresentation
from alien_tracker.tracker import Tracker


class App:
    def __init__(
        self, screen_file_path: str, threshold: float, invaders_file_paths: List[str]
    ):
        self.screen = TextFileRepresentation(screen_file_path)
        self.threshold = threshold
        self.invaders = [
            TextFileRepresentation(file_path) for file_path in invaders_file_paths
        ]

    def run(self) -> None:
        detector = SimpleDetector(self.threshold)
        tracker = Tracker(self.screen, detector, empty_value="\0")
        detections = tracker.get_detection_masks(self.invaders)
        renderer = StandardOutputRenderer()
        renderer.render(self.screen, detections)
