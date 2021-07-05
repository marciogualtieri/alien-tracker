from alien_tracker.decoders import TextFileDecoder
from alien_tracker.detectors import SimpleDetector
from alien_tracker.renderers import StandardOutputRenderer
from alien_tracker.tracker import Tracker


class App:
    def __init__(self, screen_file_path, threshold, invaders_file_paths):
        self.screen = TextFileDecoder(screen_file_path)
        self.threshold = threshold
        self.invaders = [TextFileDecoder(file_path) for file_path in invaders_file_paths]

    def run(self):
        detector = SimpleDetector(self.threshold)
        tracker = Tracker(self.screen, self.invaders, detector, empty_value="\0")
        detections = tracker.track_invaders()
        renderer = StandardOutputRenderer()
        renderer.render(self.screen, detections)
