import csv
import os
import random
import time

import schnapsen.game
import schnapsen.bots

from bot import LLMBot


class GameStats:
    did_our_bot_win: bool
    opponent_bot_id: str
    game_points_obtained: int
    score_obtained: int


def run_tournament_against_bot(
    ollama_port,
    csv_path: str,
    number_of_games: int,
    use_expert: bool,
    opponent_bot: schnapsen.game.Bot,
) -> None:
    write_header = True
    if os.path.isfile(csv_path):
        write_header = False

    file = open(csv_path, "a")
    csv_writer = csv.writer(file)
    if write_header:
        csv_writer.writerow(["did_our_bot_win", "game_points_obtained", "score_obtained"])

    engine = schnapsen.game.SchnapsenGamePlayEngine()

    our_bot = LLMBot(ollama_port, name="llmbot", use_expert=use_expert)
    opponent_bot_id = str(opponent_bot)

    print(f"-- playing {number_of_games} games against: {opponent_bot} --")
    our_win_count, opponent_win_count = 0, 0
    our_game_points, opponent_game_points = 0, 0
    our_score, opponent_score = 0, 0

    for game_number in range(number_of_games):
        print(f"playing game number {game_number+1 :<2}: ", end="")
        is_our_bot_starting = game_number % 2 == 0
        if is_our_bot_starting:
            first_bot = our_bot
            second_bot = opponent_bot
        else:
            first_bot = opponent_bot
            second_bot = our_bot

        winner_bot, game_points, score = engine.play_game(
            first_bot, second_bot, random.Random(time.time())
        )
        print(
            f"{str(winner_bot):<13} won the game, with score: {score.direct_points}, obtained: {game_points} game points"
        )

        game_stats = GameStats()
        game_stats.did_our_bot_win = winner_bot is our_bot

        game_stats.game_points_obtained = game_points
        game_stats.score_obtained = score.direct_points
        csv_writer.writerow(
            [
                game_stats.did_our_bot_win,
                game_stats.game_points_obtained,
                game_stats.score_obtained,
            ]
        )
        file.flush()

        if winner_bot is our_bot:
            our_win_count += 1
            our_game_points += game_points
            our_score += score.direct_points
        else:
            opponent_win_count += 1
            opponent_game_points += game_points
            opponent_score += score.direct_points

    print(
        f"-- our bot won {(our_win_count/number_of_games)*100:.2f}% of the games against: {opponent_bot}"
    )

    file.flush()
    file.close()
