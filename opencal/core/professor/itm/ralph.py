"""Ralph randomly pick cards. No matter the answer, each card is put back in the stack (i.e. "draw with replacement").
This professor is used for intermediate-term memory training.
"""

import random

class ProfessorRalph:

    def __init__(self, card_list):
        self._card_list = [card for card in card_list if not card["hidden"]]
        self.update_card()

    def update_card(self):
        if len(self._card_list) > 0:
            current_index = random.randint(0, len(self._card_list) - 1)
            self._current_card = self._card_list[current_index]
        else:
            self._current_card = None

    @property
    def current_card(self):
        return self._current_card

    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        self.update_card()
