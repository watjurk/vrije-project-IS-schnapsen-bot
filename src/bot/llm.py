from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, GamePhase
from schnapsen.deck import Card

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms.ollama import Ollama


class LLMBot(Bot):
    """
    Args:
        name (Optional[str]): The optional name of this bot
    """

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)

        # self.llm = Ollama(model="llama2", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
        # print(self.llm.invoke("Hello"))

    def get_move(
        self,
        perspective: PlayerPerspective,
        leader_move: Optional[Move],
    ) -> Move:
        print(perspective_to_llm_representation(perspective))
        exit(0)
        return perspective.valid_moves()[0]


def perspective_to_llm_representation(
    perspective: PlayerPerspective,
) -> str:
    representation = ""

    game_phase = ""
    if perspective.get_phase() == GamePhase.ONE:
        game_phase = "STAGE1"
    else:
        game_phase = "STAGE2"
    representation += f"The game stage: {game_phase}\n"

    seen_cards = ""
    for card in perspective.seen_cards(None):
        seen_cards += card_to_llm_representation(card) + " "
    representation += f"The cards which have been seen: {seen_cards}\n"

    your_cards = ""
    for card in perspective.get_hand().cards:
        your_cards += card_to_llm_representation(card) + " "
    representation += f"Your cards: {seen_cards}\n"

    valid_moves = ""
    for move in perspective.valid_moves():
        valid_moves += move_to_llm_representation(move) + " "
    representation += f"An array of valid moves you can take: {valid_moves}"

    return representation


def card_to_llm_representation(card: Card) -> str:
    return f"{str(card.rank)}_{str(card.suit)}"


def move_to_llm_representation(move: Move) -> str:
    if move.is_marriage():
        move = move.as_marriage()
        return f"MARRIAGE: ({card_to_llm_representation(move.cards[0]), card_to_llm_representation(move.cards[1])})"

    if move.is_trump_exchange():
        move = move.as_trump_exchange()
        return f"TRUMP_EXCHANGE: ({card_to_llm_representation(move.jack)})"

    if move.is_regular_move():
        move = move.as_regular_move()
        return f"REGULAR: ({card_to_llm_representation(move.card)})"

    assert False, "Unknown move type."
