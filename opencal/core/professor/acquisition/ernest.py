"""Professor Ernest pick cards in an "work in progress" window that is progressively moved along the full cards list.
For each right answer, the card is removed.
This teacher is used for the acquisition (or "learning phase"), i.e. the initial stage when information is introduced and learned.
"""

from opencal.core.professor.professor import AbstractProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

CARDS_IN_PROGRESS_INCREMENT_SIZE = 5

class ProfessorErnest(AbstractProfessor):

    def __init__(self, card_list, cards_in_progress_increment_size=CARDS_IN_PROGRESS_INCREMENT_SIZE):
        super().__init__()

        self._cards_not_yet_reviewed_list = []
        self._cards_in_progress_list = []

        self.cards_in_progress_increment_size = cards_in_progress_increment_size
        self.update_card_list(card_list)


    @property
    def current_card(self):
        if len(self._cards_in_progress_list) == 0:
            print()
            if self._last_card_in_progress_index < len(self._cards_not_yet_reviewed_list):
                # Update the list of cards being reviewed ("cards in progress")
                self._cards_in_progress_list = self._cards_not_yet_reviewed_list[self._last_card_in_progress_index:self._last_card_in_progress_index+self.cards_in_progress_increment_size]
                self._last_card_in_progress_index += self.cards_in_progress_increment_size
                print(f"Update the work in progress card list ; current index = {self._last_card_in_progress_index} ", end='', flush=True)
            else:
                # Review is completed
                print("Review completed")
                return None

        return self._cards_in_progress_list[0]


    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        if len(self._cards_in_progress_list) > 0:
            # Pick the first card in progress
            card = self._cards_in_progress_list.pop(0)

            if answer in ("skip", WRONG_ANSWER_STR):
                # If the answer is right or skip, put the card back to the end of the cards in progress list
                self._cards_in_progress_list.append(card)
            elif answer == RIGHT_ANSWER_STR:
                print(".", end='', flush=True)
            else:
                raise ValueError(f"Unknown answer : {answer}")


    def update_card_list(self, card_list):
        self._cards_not_yet_reviewed_list = [card for card in card_list if not card["hidden"]]
        self._cards_in_progress_list = []
        self._last_card_in_progress_index = 0
        print(f"Review {len(card_list)} cards")
