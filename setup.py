from setuptools import setup, find_packages

setup(
    name="alien-tracker",
    version="0.1.0",
    packages=find_packages(include=["alien_tracker", "alien_tracker.*"]),
    entry_points={
        "console_scripts": [
            "alien-tracker = alien_tracker.cli:main",
        ],
    },
)
