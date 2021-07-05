from abc import ABC
from abc import abstractmethod

from colored import fg, bg, attr


class Renderer(ABC):
    @abstractmethod
    def render(self, screen, detections):
        pass


class StandardOutputRenderer(Renderer):
    """
    Renders detections to standard output as colored text, each invader detection a different color.
    """

    output_reset = attr(0)
    output_background_color = bg("black")

    def render(self, screen, detections):
        screen_contents = screen.decode()
        self._print_detections(detections, screen_contents)

    def _print_detections(self, detections, screen_contents):
        rows, _ = screen_contents.shape
        for row in range(0, rows):
            self._print_detections_row(row, detections, screen_contents)

    def _print_detections_row(self, row, detections, screen_contents):
        _, cols = screen_contents.shape
        for col in range(0, cols):
            output_foreground_color = self._get_detection_foreground_color(row, col, detections)
            self._print_text(screen_contents[row][col], output_foreground_color)
        self._print_empty_line()

    def _print_empty_line(self):
        print(f"{self.output_background_color}{self.output_reset}")

    def _print_text(self, text, output_foreground_color):
        print(
            f"{output_foreground_color}{self.output_background_color}{text}{self.output_reset}",
            end="")

    @staticmethod
    def _get_detection_foreground_color(row, col, detections):
        first_color_code = 1
        color_codes = list(range(first_color_code, len(detections) + 1))
        for detection, color in zip(detections, color_codes):
            if detection[row][col]:
                return fg(color)
        return fg("white")
