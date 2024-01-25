import random
import time

import click

import schnapsen.bots

from tournament import run_tournament_against_bot


@click.command()
@click.option("number_of_games", "-n", "--number", default=20, help="Number of games to play.")
@click.option("csv_path", "-c", "--csv", help="CSV file path.", required=True)
@click.option(
    "opponent_bot_id",
    "-b",
    "--bot",
    type=click.Choice(["Rdeep", "Rand"], case_sensitive=False),
    help="Bot to play against.",
    required=True,
)
def run_tournament(number_of_games, csv_path, opponent_bot_id):
    if opponent_bot_id == "Rdeep":
        opponent_bot = schnapsen.bots.RdeepBot(
            num_samples=2, depth=4, rand=random.Random(time.time()), name="rdeep"
        )

    if opponent_bot_id == "Rand":
        opponent_bot = schnapsen.bots.RandBot(random.Random(time.time()), name="rand")

    run_tournament_against_bot(csv_path, number_of_games, opponent_bot)


if __name__ == "__main__":
    run_tournament()
