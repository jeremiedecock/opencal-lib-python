"""Alice is an implementation of the "classical" flashcard method.
This professor is mostly used for short term memory training.
"""

import copy
import random

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

class ProfessorAlice:

    def __init__(self, card_list):
        self._card_list = copy.copy(card_list)
        random.shuffle(self._card_list)

    @property
    def current_card(self):
        return self._card_list[0] if len(self._card_list) > 0 else None

    def current_card_reply(self, answer):
        if len(self._card_list) > 0:
            card = self._card_list.pop(0)

            if answer == WRONG_ANSWER_STR:
                self._card_list.append(card)
            elif answer == RIGHT_ANSWER_STR:
                pass
            else:
                raise ValueError("Unknown answer : {}".format(answer))