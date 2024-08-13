import sqlite3
from typing import Optional
import warnings

import opencal
from opencal.io.sqlitedb import ACQUISITION_REVIEW_TABLE_NAME

class AbstractProfessor:

    def __init__(self):
        self.observer_list = []

        self.opencal_db_path: str = opencal.cfg['opencal']['db_path']
        self.opencal_db_path = opencal.path.expand_path(self.opencal_db_path)

        self.con: sqlite3.Connection = sqlite3.connect(self.opencal_db_path)
        self.cur: sqlite3.Cursor = self.con.cursor()
    
    def __del__(self):
        self.con.close()

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
        raise NotImplementedError()

    @property
    def remaining_cards(self) -> float:
        return float("inf")      # Some professor may ask the same questions for an infinite (or unpredictable) number of times
