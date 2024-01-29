import random
import time

import click

import schnapsen.bots

from tournament import run_tournament_against_bot


@click.command()
@click.option("number_of_games", "-n", "--number", default=20, help="Number of games to play.")
@click.option("ollama_port", "-p", "--port", default=11434, help="Ollama's port")
@click.option("use_expert", "-u", "--use_expert", type=bool, help="Should the llm use expert.")
@click.option("csv_path", "-c", "--csv", help="CSV file path.", required=True)
def run_tournament(ollama_port, number_of_games, use_expert, csv_path):
    opponent_bot = schnapsen.bots.RdeepBot(
        num_samples=2, depth=4, rand=random.Random(time.time()), name="rdeep"
    )
    run_tournament_against_bot(ollama_port, csv_path, number_of_games, use_expert, opponent_bot)


if __name__ == "__main__":
    run_tournament()
