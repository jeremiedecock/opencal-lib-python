"""Professor Charles randomly picks cards in an "active set" that is progressively widened.
For each right answer, the card is removed.
This teacher is used for the acquisition (or "learning phase"), i.e. the initial stage when information is introduced and learned.

On a M cartes ; on en tire 5 au hazard (sans remise) -> c'est l'ensemble des cartes "actives".
Chacune des cartes a un historiques de réponses : une liste de booléens initialement vide
(1 = bonne réponse ; 0 = mauvaise réponse).
Pour chaque carte active, on ne regarde que les 3 derniers résultats.
Ces 3 résultats servent à calculer un score pour chaque carte active:

score = 1/7 * r3 + 2/7 * r2 + 4/7 * r1

avec historique des résultats = [..., r3, r2, r1]

ri \in {0; 1}
score \in [0;1]

Ce score sert à 2 choses:
- définir s'il faut ajouter une carte à l'ensemble des cartes actives
  si toutes les cartes ont un score >= 6/7 alors ajouter une carte
- définir le poids de chaque carte chaque fois qu'on tire aléatoirement
  une carte de l'ensemble actif pour l'intérroger
  proba carte i = (1 - score i)/(sum_j(1 - score j))
"""

import random

from opencal.core.professor.acquisition.professor import AbstractAcquisitionProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR
from typing import Optional

ACTIVE_SET_SIZE = 3
REVIEWS_HORIZON = 3
WIDENING_THRESHOLD = 3 # 1.

# TODO : passer les 3 constantes prec dans le fichier de config YAML
# TODO : pondérer le poids des réponses dans le score des cartes (facteur d'escompte)

class ProfessorCharles(AbstractAcquisitionProfessor):

    def __init__(self, card_list):
        super().__init__()

        self.update_card_list(card_list)
        self._current_card = None
        self._full_card_set = None
        self._active_card_set = None


    @property
    def current_card(self):
        return self._current_card


    def _update_card(self):
        if len(self._active_card_set) > 0:
            scores = [card['charles_score'] for card in self._active_card_set]
            do_widen = all([score >= WIDENING_THRESHOLD for score in scores])

            if do_widen and (len(self._active_card_set) == len(self._full_card_set)):

                self._current_card = None

            elif do_widen:

                remaining_set = self._full_card_set - self._active_card_set
                new_active_card = random.sample(remaining_set, k=1)[0]
                self._current_card = new_active_card

            else:

                weights = [1. - score for score in scores]
                self._current_card = random.choices(tuple(self._active_card_set), weights=weights)[0]

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

        result = 1 if answer == RIGHT_ANSWER_STR else 0

        if self._current_card is not None:
            self._current_card['charles_reviews'].append(result)
            self._current_card['charles_score'] = sum(self._current_card['charles_reviews'][:-REVIEWS_HORIZON]) #/ min(len(self._current_card['charles_reviews']), REVIEWS_HORIZON)

        self._update_card()


    def update_card_list(
            self,
            card_list: list,
            review_hidden_cards: bool = False
        ):
        self._full_card_set = {card for card in card_list if ((not card["hidden"]) or review_hidden_cards)}

        # Init cards
        for card in self._full_card_set:
            self._current_card['charles_reviews'] = []
            self._current_card['charles_score'] = 0

        # Random sampling without replacement
        self._active_card_set = set(random.sample(self._full_card_set,
                                                  k=min(len(self._full_card_set), ACTIVE_SET_SIZE)))

        self._update_card()
