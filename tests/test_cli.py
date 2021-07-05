from click.testing import CliRunner

from alien_tracker.cli import cli
from .test_case_helper import TestCaseHelper


class TestCLI(TestCaseHelper):
    @classmethod
    def setUpClass(cls):
        cls.screen = cls.get_test_resource_full_path("screens", "sample-screen.txt")
        cls.squid = cls.get_test_resource_full_path("invaders", "squid.txt")
        cls.crab = cls.get_test_resource_full_path("invaders", "crab.txt")
        cls.threshold = 0.75

    def test_track_multiple_invaders(self):
        output = self.get_test_resource_contents(
            "screens", "sample-screen-output-2-invaders.txt"
        )
        result = self.run_cli(
            ["-s", self.screen, "-t", self.threshold, "-i", self.squid, "-i", self.crab]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(output, result.output)

    def test_track_multiple_invaders_higher_threshold(self):
        output = self.get_test_resource_contents(
            "screens", "sample-screen-output-2-invaders-0-8-threshold.txt"
        )
        result = self.run_cli(
            ["-s", self.screen, "-t", 0.8, "-i", self.squid, "-i", self.crab]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(output, result.output)

    def test_track_single_invader(self):
        output = self.get_test_resource_contents(
            "screens", "sample-screen-output-1-invader.txt"
        )
        result = self.run_cli(
            ["-s", self.screen, "-t", self.threshold, "-i", self.squid]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(output, result.output)

    @staticmethod
    def run_cli(arguments):
        runner = CliRunner()
        return runner.invoke(cli, arguments)
