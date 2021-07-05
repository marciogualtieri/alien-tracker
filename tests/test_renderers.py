import contextlib
import io

import numpy as np

from alien_tracker.renderers import StandardOutputRenderer
from alien_tracker.representations import TextRepresentation
from .test_case_helper import TestCaseHelper


class TestRenderers(TestCaseHelper):
    def test_standard_output_renderer(self):
        renderer = StandardOutputRenderer()

        test_screen = TextRepresentation(
            """
                                  abcd
                                  efgh
                                  ijkl
                                  mnop
                                  """
        )

        test_detections = [
            np.array(
                [
                    [True, True, False, False],
                    [True, True, False, False],
                    [False, False, False, False],
                    [False, False, False, False],
                ]
            ),
            np.array(
                [
                    [False, False, False, False],
                    [False, False, False, False],
                    [False, False, True, True],
                    [False, False, True, True],
                ]
            ),
        ]

        rendered_colored_output = self.get_test_resource_contents(
            "screens", "simple-output.txt"
        )

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            renderer.render(test_screen, test_detections)
            self.assertIn(rendered_colored_output, mock_stdout.getvalue())
