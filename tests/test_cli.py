from click.testing import CliRunner

from alien_tracker import cli
from .test_case_helper import TestCaseHelper


class TestCLI(TestCaseHelper):

    def setUp(self):
        self.screen = self.get_test_resource_full_path("screens", "sample-screen.txt")
        self.squid = self.get_test_resource_full_path("invaders", "squid.txt")
        self.crab = self.get_test_resource_full_path("invaders", "crab.txt")
        self.threshold = 0.75

    def test_track_multiple_invaders(self):
        runner = CliRunner()
        output = self.get_test_resource_contents("screens", "sample-screen-output-multiple-invaders.txt")
        result = runner.invoke(cli, ["-s", self.screen, "-t", self.threshold, "-i", self.squid, "-i", self.crab])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(output, result.output)

    def test_track_single_invader(self):
        runner = CliRunner()
        output = self.get_test_resource_contents("screens", "sample-screen-output-single-invader.txt")
        result = runner.invoke(cli, ["-s", self.screen, "-t", self.threshold, "-i", self.squid])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(output, result.output)
