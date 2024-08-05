"""Ralph randomly pick cards. No matter the answer, each card is put back in the stack (i.e. "draw with replacement").
This teacher is used for the acquisition (or "learning phase"), i.e. the initial stage when information is introduced and learned.
"""

from opencal.core.professor.acquisition.professor import AbstractAcquisitionProfessor
import random

class ProfessorRalph(AbstractAcquisitionProfessor):

    def __init__(self, card_list):
        super().__init__()

        self.update_card_list(card_list)
        self._current_card = None

    @property
    def current_card(self):
        return self._current_card

    def update_card(self):
        if len(self._card_list) > 0:
            self._current_card = random.choice(self._card_list)
        else:
            self._current_card = None

    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        self.update_card()

    def update_card_list(self, card_list):
        self._card_list = [card for card in card_list if not card["hidden"]]
        self.update_card()
