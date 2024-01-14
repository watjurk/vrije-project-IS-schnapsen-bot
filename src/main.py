import random
import time

import schnapsen.game
import schnapsen.bots

import bot.llm

engine = schnapsen.game.SchnapsenGamePlayEngine()

random_bot = schnapsen.bots.RandBot(random.Random(time.time()), "random_bot")
llm_bot = bot.LLMBot("llm_bot")

game_rand = random.Random(time.time())
winner, points_obtained, game_score = engine.play_game(random_bot, llm_bot, game_rand)
print(winner, points_obtained, game_score)
