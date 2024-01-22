from typing import Optional, List, Tuple
from enum import Enum, auto
from schnapsen.game import Bot, PlayerPerspective, Move, GamePhase, Trick
from schnapsen.deck import Card

from . import llm_engine


class LLMBot(Bot):
    """
    Args:
        name (Optional[str]): The optional name of this bot
    """

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)

    def get_move(
        self,
        perspective: PlayerPerspective,
        leader_move: Optional[Move],
    ) -> Move:
        print()
        print()
        print("---------- THE GAME VIEW FOR LLM -----")
        print(perspective_to_llm_representation(perspective, leader_move))
        print("---------- THE GAME VIEW FOR LLM -----")
        print()
        print()

        # print("Send game state to LLM bot")
        game_state = perspective_to_llm_representation(perspective, leader_move)

        while True:
            print(game_state)
            llm_output = llm_engine.generate(game_state)

            print()
            print(llm_output)
            print()

            ok, move, parsing_err = parse_llm_output(
                perspective.valid_moves(), llm_output
            )
            if ok:
                break

            print(parsing_err)
            print()

        assert move is not None
        return move

        # MOVE_QUESTION_ID = "move"
        # valid_moves_as_string = [
        #     move_to_llm_representation(move) for move in perspective.valid_moves()
        # ]
        # choose_move_questions = inquirer.List(
        #     MOVE_QUESTION_ID,
        #     message="CHOOSE THE LLM'S MOVE",
        #     choices=valid_moves_as_string,
        # )

        # answers = inquirer.prompt([choose_move_questions])
        # assert answers is not None, "inquirer.prompt returned None as answers."

        # move_answer = answers[MOVE_QUESTION_ID]
        # move_index = valid_moves_as_string.index(move_answer)
        # return perspective.valid_moves()[move_index]


class ParseLLMOutputError(Enum):
    MORE_THAN_ONE_MOVE_MATCHES = auto()
    NO_MOVE_MATCHES = auto()


def parse_llm_output(
    valid_moves: List[Move], llm_output: str
) -> Tuple[bool, Optional[Move], Optional[ParseLLMOutputError]]:
    matching_moves = []

    for move in valid_moves:
        matching_moves.append(move_to_llm_representation(move) in llm_output)

    if matching_moves.count(True) == 0:
        return False, None, ParseLLMOutputError.NO_MOVE_MATCHES

    if matching_moves.count(True) > 1:
        return False, None, ParseLLMOutputError.MORE_THAN_ONE_MOVE_MATCHES

    matching_move_index = matching_moves.index(True)
    return True, valid_moves[matching_move_index], None


def perspective_to_llm_representation(
    perspective: PlayerPerspective,
    leader_move: Optional[Move],
) -> str:
    representation = ""

    history_representation = history_to_llm_representation(
        perspective.get_game_history()
    )
    representation += "GAME HISTORY:\n"
    representation += f"{history_representation}\n"

    representation += "GAME STATE:\n"
    game_phase = ""
    if perspective.get_phase() == GamePhase.ONE:
        game_phase = "STAGE1"
    else:
        game_phase = "STAGE2"
    representation += f"The game stage: {game_phase}\n"

    representation += f"The trump suit is: {str(perspective.get_trump_suit())}\n"
    if perspective.get_trump_card() is not None:
        representation += f"The trump card is: {card_to_llm_representation(perspective.get_trump_card())}\n"

    seen_cards = ""
    for card in perspective.seen_cards(None):
        seen_cards += card_to_llm_representation(card) + " "
    representation += f"The cards which have been seen: {seen_cards}\n"

    your_cards = ""
    for card in perspective.get_hand().cards:
        your_cards += card_to_llm_representation(card) + " "
    representation += f"Your cards: {seen_cards}\n"

    leader_move_representation = ""
    if leader_move == None:
        leader_move_representation = "You are the leader"
    else:
        leader_move_representation = f"Your opponent is the leader. Your opponent made this move: {move_to_llm_representation(leader_move)}"
    representation += f"{leader_move_representation}\n"

    valid_moves = ""
    for move in perspective.valid_moves():
        valid_moves += move_to_llm_representation(move) + " "
    representation += f"An array of valid moves you can take: {valid_moves}"

    return representation


def history_to_llm_representation(
    game_history: list[tuple[PlayerPerspective, Optional[Trick]]]
) -> str:
    history_representation = ""
    my_previous_score = 0

    for i, (perspective, trick) in enumerate(game_history):
        if trick is None:
            continue

        try:
            my_next_score = game_history[i + 1][0].get_my_score().direct_points
        except:
            my_next_score = 0

        did_i_win_the_trick = False
        if my_next_score > my_previous_score:
            did_i_win_the_trick = True
        my_previous_score = my_next_score

        history_representation += "\n"
        if trick.is_trump_exchange():
            history_representation += "TRUMP EXCHANGE"
            continue

        if perspective.am_i_leader():
            my_move = trick.leader_move
            opponent_move = trick.follower_move
            history_representation += "You were the leader.\n"
            history_representation += (
                f"You played: {move_to_llm_representation(my_move)}\n"
            )
            history_representation += (
                f"Your opponent played: {move_to_llm_representation(opponent_move)}\n"
            )
        else:
            my_move = trick.follower_move
            opponent_move = trick.leader_move
            history_representation += "Your opponent was the leader.\n"
            history_representation += (
                f"You played: {move_to_llm_representation(my_move)}\n"
            )
            history_representation += (
                f"Your opponent played: {move_to_llm_representation(opponent_move)}\n"
            )

        if did_i_win_the_trick:
            history_representation += "You won this trick.\n"
        else:
            history_representation += "Your opponent won this trick.\n"

    return history_representation[1:]


def card_to_llm_representation(card: Card) -> str:
    return f"{str(card.rank)}_{str(card.suit)}"


def move_to_llm_representation(move: Move) -> str:
    if move.is_marriage():
        move = move.as_marriage()
        return f"MARRIAGE: ({card_to_llm_representation(move.cards[0])}, {card_to_llm_representation(move.cards[1])})"

    if move.is_trump_exchange():
        move = move.as_trump_exchange()
        return f"TRUMP_EXCHANGE: ({card_to_llm_representation(move.jack)})"

    if move.is_regular_move():
        move = move.as_regular_move()
        return f"REGULAR: ({card_to_llm_representation(move.card)})"

    assert False, "Unknown move type."
