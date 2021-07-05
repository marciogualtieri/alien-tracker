import click

from alien_tracker.app import App


@click.command()
@click.option(
    "--screen", "-s", required=True, help="Path to a text file with the screen"
)
@click.option(
    "--threshold",
    "-t",
    required=True,
    type=float,
    help="Detection threshold in the interval (0.0, 1.0)",
)
@click.option(
    "--invaders",
    "-i",
    required=True,
    multiple=True,
    help="Path to a text file with an invader. Multiple invaders might be provided",
)
def cli(screen, threshold, invaders) -> None:
    app = App(screen, threshold, invaders)
    app.run()


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
