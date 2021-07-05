from os import path
from unittest import TestCase


class TestCaseHelper(TestCase):
    @staticmethod
    def get_test_resource_full_path(*relative_path):
        test_resources_path = path.dirname(__file__)
        return path.join(test_resources_path, "resources", *relative_path)

    @classmethod
    def get_test_resource_contents(cls, *relative_path):
        test_resource_full_path = cls.get_test_resource_full_path(*relative_path)
        with open(test_resource_full_path, "r") as f:
            return f.read()
