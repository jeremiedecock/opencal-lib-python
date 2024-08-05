"""Brutus pick all cards. For each right answer, the card is removed.
This teacher is only used for the in the ForwardTest tab.
"""

import datetime

from opencal.core.professor.professor import AbstractProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR
from typing import Optional

class ProfessorBrutus(AbstractProfessor):

    def __init__(self, card_list, date_mock=None):
        super().__init__()

        self.update_card_list(card_list)

        if date_mock is None:
            self._date = datetime.date
        else:
            self._date = date_mock


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

            if answer == RIGHT_ANSWER_STR:
                review = {
                    "rdate": self._date.today(),
                    "result": RIGHT_ANSWER_STR
                }
                card["reviews"].append(review)
            elif answer == WRONG_ANSWER_STR:
                review = {
                    "rdate": self._date.today(),
                    "result": WRONG_ANSWER_STR
                }
                card["reviews"].append(review)
            elif answer == "skip":
                pass
            elif answer == "skip level":
                pass
            else:
                raise ValueError(f"Unknown answer : {answer}")

            if hide:
                card["hidden"] = True

            self.notify_observers_of_reply()


    def update_card_list(
            self,
            card_list: list,
            review_hidden_cards: bool = False
        ):
        self._card_list = [card for card in card_list if ((not card["hidden"]) or review_hidden_cards)]
        #self.notify_observers()


    @property
    def remaining_cards(self):
        return len(self._card_list)
