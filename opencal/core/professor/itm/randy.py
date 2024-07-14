"""Randy randomly pick cards. For each right answer, the card is removed.
This professor is used for intermediate-term memory training.
"""

import copy
import random

from opencal.core.professor.professor import AbstractProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

class ProfessorRandy(AbstractProfessor):

    def __init__(self, card_list):
        super().__init__()

        self.update_card_list(card_list)

        # Shuffle list `self._card_list` in place and return None
        random.shuffle(self._card_list)

    @property
    def current_card(self):
        return self._card_list[0] if len(self._card_list) > 0 else None

    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
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

    def update_card_list(self, card_list):
        self._card_list = [card for card in card_list if not card["hidden"]]
