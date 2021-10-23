"""Professor Arthur pick cards in an "active set" that is progressively widened.
For each right answer, the card is removed.
This professor is used for intermediate-term memory training.
"""

from opencal.core.professor.professor import AbstractProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

DEFAULT_ACTIVE_LIST_INCREMENT_SIZE = 5

# TODO : passer la constante prec dans le fichier de config YAML

class ProfessorArthur(AbstractProfessor):

    def __init__(self, card_list, active_list_increment_size=DEFAULT_ACTIVE_LIST_INCREMENT_SIZE):
        super().__init__()

        self.active_list_increment_size = active_list_increment_size
        self.update_card_list(card_list)


    @property
    def current_card(self):
        if len(self._active_card_list) == 0:
            print()
            if self._active_card_list_size < len(self._full_card_list):
                # The active card list is incremented
                self._active_card_list_size += self.active_list_increment_size
                self._active_card_list = self._full_card_list[:self._active_card_list_size]
                print("Widen the active card list ; current size = {:3d} ".format(len(self._active_card_list)), end='', flush=True)
            else:
                # review is completed
                print("Review completed")
                return None

        return self._active_card_list[0]


    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        if len(self._active_card_list) > 0:
            card = self._active_card_list.pop(0)

            if answer in ("skip", WRONG_ANSWER_STR):
                self._active_card_list.append(card)
            elif answer == RIGHT_ANSWER_STR:
                print(".", end='', flush=True)
            else:
                raise ValueError("Unknown answer : {}".format(answer))


    def update_card_list(self, card_list):
        self._full_card_list = [card for card in card_list if not card["hidden"]]
        self._active_card_list = []
        self._active_card_list_size = 0
        print("Review {:d} cards".format(len(card_list)))
