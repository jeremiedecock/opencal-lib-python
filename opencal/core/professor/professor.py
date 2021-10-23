import warnings

class AbstractProfessor:
    def __init__(self):
        self.observer_list = []

    # ANSWER CALLBACK #################

    def add_reply_observer(self, observer):
        self.observer_list.append(observer)
        #print("Num observers:", len(self.observer_list))

    def remove_reply_observer(self, observer):
        try:
            self.observer_list.remove(observer)
        except ValueError as err:
            warnings.warn("observer" + str(observer) + " not in prof " + str(self) + "\n" + str(err))
        #print("Num observers:", len(self.observer_list))

    def notify_observers_of_reply(self):
        """This function is supposed to be called after each reply"""
        for observer in self.observer_list:
            observer.answer_callback()

    ###################################

    @property
    def current_card(self):
        raise NotImplementedError()

    @property
    def remaining_cards(self):
        return float("inf")      # Some professor may ask the same questions for an infinite (or unpredictable) number of times

    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        raise NotImplementedError()
