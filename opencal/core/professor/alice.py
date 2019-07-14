"""Alice is an implementation of the "classical" flashcard method.
This professor is mostly used for short term memory training.
"""

import copy
import random

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

class ProfessorAlice:

    def __init__(self, card_list): #, date_mock=None):
        self._card_list = [card for card in card_list if not card["hidden"]]

        # Shuffle list `self._card_list` in place and return None
        random.shuffle(self._card_list)

        # if date_mock is None:
        #     self._date = datetime.date
        # else:
        #     self._date = date_mock

    @property
    def current_card(self):
        return self._card_list[0] if len(self._card_list) > 0 else None

    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        if len(self._card_list) > 0:
            card = self._card_list.pop(0)

            if answer == "skip":
                # if not hide:
                self._card_list.append(card)
            elif answer == RIGHT_ANSWER_STR:
                pass
                # review = {
                #     "rdate": self._date.today(),
                #     "result": RIGHT_ANSWER_STR
                # }
                # card["reviews"].append(review)
            elif answer == WRONG_ANSWER_STR:
                self._card_list.append(card)
                # review = {
                #     "rdate": self._date.today(),
                #     "result": WRONG_ANSWER_STR
                # }
                # card["reviews"].append(review)
            else:
                raise ValueError("Unknown answer : {}".format(answer))

            # if hide:
            #     card["hidden"] = True