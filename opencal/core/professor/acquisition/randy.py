"""Randy randomly pick cards. For each right answer, the card is removed.
This teacher is used for the acquisition (or "learning phase"), i.e. the initial stage when information is introduced and learned.
"""

import copy
import random

from opencal.core.professor.acquisition.professor import AbstractAcquisitionProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR
from typing import Optional

class ProfessorRandy(AbstractAcquisitionProfessor):

    def __init__(self, card_list):
        super().__init__()

        self.update_card_list(card_list)

        # Shuffle list `self._card_list` in place and return None
        random.shuffle(self._card_list)

    @property
    def current_card(self):
        return self._card_list[0] if len(self._card_list) > 0 else None

    def current_card_reply(
            self,
            answer: str,
            hide: bool = False,
            user_response_time_ms: Optional[int] = None,
            confidence: Optional[float] = None
        ) -> None:
        """
        Handle the reply to the current card.

        Parameters
        ----------
        answer : str
            The answer provided by the user.
        hide : bool, optional
            Whether to hide the card after the reply (default is False).
        user_response_time_ms : Optional[int], optional
            The time taken by the user to respond, in milliseconds (default is None).
        confidence : Optional[float], optional
            The confidence level of the user's answer (default is None).

        Returns
        -------
        None
            This function does not return any value.
        """

        if len(self._card_list) > 0:
            card = self._card_list.pop(0)

            if answer == "skip":
                self._card_list.append(card)
            elif answer == RIGHT_ANSWER_STR:
                pass
            elif answer == WRONG_ANSWER_STR:
                self._card_list.append(card)
            else:
                raise ValueError(f"Unknown answer : {answer}")

    def update_card_list(
            self,
            card_list: list,
            review_hidden_cards: bool = False
        ):
        self._card_list = [card for card in card_list if ((not card["hidden"]) or review_hidden_cards)]
