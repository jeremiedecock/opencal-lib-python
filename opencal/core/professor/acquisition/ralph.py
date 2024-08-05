"""Ralph randomly pick cards. No matter the answer, each card is put back in the stack (i.e. "draw with replacement").
This teacher is used for the acquisition (or "learning phase"), i.e. the initial stage when information is introduced and learned.
"""

from opencal.core.professor.acquisition.professor import AbstractAcquisitionProfessor
import random
from typing import Optional

class ProfessorRalph(AbstractAcquisitionProfessor):

    def __init__(self, card_list):
        super().__init__()

        self.update_card_list(card_list)
        self._current_card = None

    @property
    def current_card(self):
        return self._current_card

    def _update_card(self):
        if len(self._card_list) > 0:
            self._current_card = random.choice(self._card_list)
        else:
            self._current_card = None

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
        self._update_card()

    def update_card_list(
            self,
            card_list: list,
            review_hidden_cards: bool = False
        ):
        self._card_list = [card for card in card_list if ((not card["hidden"]) or review_hidden_cards)]
        self._update_card()
