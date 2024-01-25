import click

import random
import time

import schnapsen.game
import schnapsen.bots

from bot import LLMBot


@click.command()
@click.option("-n", "--number", default=20, help="Number of games to play against each bot.")
def run_tournament(number):
    number_of_games_against_each_bot = number
    engine = schnapsen.game.SchnapsenGamePlayEngine()

    our_bot = LLMBot(name="llmbot")
    # our_bot = schnapsen.bots.RandBot(rand=random.Random(time.time()), name="our_randbot")
    # out_bot_id = str(our_bot)

    bot1 = schnapsen.bots.RandBot(rand=random.Random(time.time()), name="randbot")
    bot2 = schnapsen.bots.RdeepBot(num_samples=2, depth=4, rand=random.Random(time.time()), name="rdeepbot")
    bots_to_play_against = [bot1, bot2]

    # all_bots_in_tournament = [our_bot]
    # all_bots_in_tournament.extend(bots_to_play_against)

    total_games = number_of_games_against_each_bot * len(bots_to_play_against)
    print(f"---- playing {total_games} games ----")
    print(f"---- {number_of_games_against_each_bot} games against each bot ----")

    our_total_win_count = 0

    for bot in bots_to_play_against:
        print()
        print(f"-- playing against {bot} --")
        our_win_count, opponent_win_count = 0, 0
        our_game_points, opponent_game_points = 0, 0
        our_score, opponent_score = 0, 0

        for game_number in range(number_of_games_against_each_bot):
            print(f"playing game number {game_number+1 :<2}: ", end="")
            is_our_bot_starting = random.choice([True, False])
            if is_our_bot_starting:
                first_bot = our_bot
                second_bot = bot
            else:
                first_bot = bot
                second_bot = our_bot

            winner_bot, game_points, score = engine.play_game(first_bot, second_bot, random.Random(time.time()))
            print(f"{str(winner_bot):<13} won the game, with score: {score.direct_points}, obtained: {game_points} game points")

            if winner_bot is our_bot:
                our_win_count += 1
                our_game_points += game_points
                our_score += score.direct_points
            else:
                opponent_win_count += 1
                opponent_game_points += game_points
                opponent_score += score.direct_points

        our_total_win_count += our_win_count
        print()
        print(f"-- stats against {bot} --")
        print(f"-- we won {(our_win_count/number_of_games_against_each_bot)*100:.2f}% of the games")
        # print(f"-- we won {our_win_count} out of {number_of_games_against_each_bot} games --")
        print(f"-- our game points: {our_game_points}, opponent game points: {opponent_game_points} --")
        print(f"-- our score: {our_score}, opponent score: {opponent_score} score --")

    print()
    print(f"---- in total we won {(our_total_win_count/total_games)*100:.2f}% of the games ----")


if __name__ == "__main__":
    run_tournament()
