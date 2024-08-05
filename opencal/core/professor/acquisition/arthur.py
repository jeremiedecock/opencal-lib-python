"""Professor Arthur pick cards in an "work in progress" window that is progressively moved along the full cards list.
For each right answer, the card is removed.
This teacher is used for the acquisition (or "learning phase"), i.e. the initial stage when information is introduced and learned.
"""

from opencal.core.professor.acquisition.professor import AbstractAcquisitionProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

DEFAULT_CARDS_IN_PROGRESS_INCREMENT_SIZE = 5
DEFAULT_RIGHT_ANSWERS_RATE_THRESHOLD = 0.5

class ProfessorArthur(AbstractAcquisitionProfessor):

    def __init__(self, card_list, cards_in_progress_increment_size=DEFAULT_CARDS_IN_PROGRESS_INCREMENT_SIZE, right_answers_rate_threshold=DEFAULT_RIGHT_ANSWERS_RATE_THRESHOLD):
        super().__init__()

        self._cards_not_yet_reviewed_list = []
        self._cards_in_progress_list = []
        self._num_right_answers = []          # the total number of right answers for each card
        self._num_wrong_answers = []          # the total number of wrong answers for each card

        self.cards_in_progress_increment_size = cards_in_progress_increment_size
        self.right_answers_rate_threshold = right_answers_rate_threshold
        self.update_card_list(card_list)


    @property
    def current_card(self):
        if len(self._cards_in_progress_list) == 0:
            print()
            if self._last_card_in_progress_index < len(self._cards_not_yet_reviewed_list):
                # Update the list of cards being reviewed ("cards in progress")
                reviewed_cards_list = self._cards_not_yet_reviewed_list[:self._last_card_in_progress_index]
                self._cards_in_progress_list = self._cards_not_yet_reviewed_list[self._last_card_in_progress_index:self._last_card_in_progress_index+self.cards_in_progress_increment_size]
                self._last_card_in_progress_index += self.cards_in_progress_increment_size

                # Add to self._cards_in_progress_list the less well known cards from reviewed_cards_list
                for (card_index, card) in reviewed_cards_list:
                    right_answers_rate = self._num_right_answers[card_index] / (self._num_right_answers[card_index] + self._num_wrong_answers[card_index])
                    if right_answers_rate <= self.right_answers_rate_threshold:
                        self._cards_in_progress_list.append((card_index, card))
                print(f"Update the work in progress card list ; current index = {self._last_card_in_progress_index} ; len cards_in_progress_list = { len(self._cards_in_progress_list) }", end='', flush=True)
            else:
                # Review is completed
                print("Review completed")
                return None

        return self._cards_in_progress_list[0][1]


    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):

        if len(self._cards_in_progress_list) > 0:
            # Pick the first card in progress
            (card_index, card) = self._cards_in_progress_list.pop(0)

            if answer in ("skip", WRONG_ANSWER_STR):
                # If the answer is right or skip, put the card back to the end of the cards in progress list
                self._num_wrong_answers[card_index] += 1
                self._cards_in_progress_list.append((card_index, card))
            elif answer == RIGHT_ANSWER_STR:
                self._num_right_answers[card_index] += 1
                print(".", end='', flush=True)
            else:
                raise ValueError(f"Unknown answer : {answer}")

            # Save the reply in the SQL database
            if answer in (RIGHT_ANSWER_STR, WRONG_ANSWER_STR):
                is_right_answer = answer == RIGHT_ANSWER_STR
                review_duration_ms = duration if duration is not None else -1   # TODO ?
                self.save_current_card_reply(
                    card=card,
                    review_duration_ms=review_duration_ms,
                    is_right_answer=is_right_answer
                )


    def update_card_list(self, card_list):
        self._cards_not_yet_reviewed_list = [(card_index, card) for (card_index, card) in enumerate(card_list) if not card["hidden"]]
        self._cards_in_progress_list = []
        self._num_right_answers = [0 for card in card_list if not card["hidden"]]          # the total number of right answers for each card
        self._num_wrong_answers = [0 for card in card_list if not card["hidden"]]          # the total number of wrong answers for each card
        self._last_card_in_progress_index = 0
        print(f"Review {len(card_list)} cards")
