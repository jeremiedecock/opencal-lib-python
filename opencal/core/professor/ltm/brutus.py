"""Brutus pick all cards. For each right answer, the card is removed.
This professor is used for intermediate-term memory training.
"""

import datetime

from opencal.core.professor.professor import AbstractProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

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


    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
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
                raise ValueError("Unknown answer : {}".format(answer))

            if hide:
                card["hidden"] = True

            self.notify_observers_of_reply()


    def update_card_list(self, card_list, review_hidden_cards: bool = False):
        self._card_list = [card for card in card_list if ((not card["hidden"]) or review_hidden_cards)]
        #self.notify_observers()


    @property
    def remaining_cards(self):
        return len(self._card_list)
