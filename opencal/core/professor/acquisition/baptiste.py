"""Professor Arthur randomly pick cards in an "active set".
For each right answer, the card is removed.
This teacher is used for the acquisition (or "learning phase"), i.e. the initial stage when information is introduced and learned.

Version plus simple d'Arthur.
Chaque fois qu'une carte dépasse le seuil de score,
elle est éjectée de l'active set et est remplacée par
une nouvelle carte.
"""

import random

from opencal.core.professor.professor import AbstractProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

ACTIVE_SET_SIZE = 5
REVIEWS_HORIZON = 3
SCORE_THRESHOLD = REVIEWS_HORIZON

# TODO : passer les 3 constantes prec dans le fichier de config YAML

class ProfessorBaptiste(AbstractProfessor):

    def __init__(self, card_list):
        super().__init__()

        self.update_card_list(card_list)
        self._current_card = None
        self._remaining_card_list = None
        self._active_card_list = None


    @property
    def current_card(self):
        return self._current_card


    def update_card(self):
        if len(self._active_card_list) > 0:
            scores = [card['baptiste_score'] for card in self._active_card_list]

            for card_index, score in enumerate(scores):
                if score >= SCORE_THRESHOLD:
                    self._active_card_list[card_index] = self._remaining_card_list.pop()

            weights = [1. - card['baptiste_score'] for card in self._active_card_list]
            self._current_card = random.choices(self._active_card_list, weights=weights)[0]
        else:
            self._current_card = None


    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        result = 1 if answer == RIGHT_ANSWER_STR else 0

        if self._current_card is not None:
            self._current_card['baptiste_reviews'].append(result)
            self._current_card['baptiste_score'] = sum(self._current_card['baptiste_reviews'][:-REVIEWS_HORIZON])

        self.update_card()


    def update_card_list(self, card_list):
        self._remaining_card_list = [card for card in card_list if not card["hidden"]]
        random.shuffle(self._remaining_card_list)

        # Init cards
        for card in self._remaining_card_list:
            self._current_card['baptiste_reviews'] = []
            self._current_card['baptiste_score'] = 0

        self._active_card_list = []
        while len(self._remaining_card_list) > 0 and len(self._active_card_list) < ACTIVE_SET_SIZE:
            self._active_card_list.append(self._remaining_card_list.pop())

        self.update_card()
