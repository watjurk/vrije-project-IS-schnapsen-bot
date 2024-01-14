import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move


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
        return perspective.valid_moves()[0]
