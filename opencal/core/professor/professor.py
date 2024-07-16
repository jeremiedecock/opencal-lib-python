import datetime
import opencal
from opencal.io.sqlitedb import ITM_REVIEW_TABLE_NAME
import sqlite3
import warnings

class AbstractProfessor:

    def __init__(self):
        self.observer_list = []

        self.opencal_db_path = opencal.cfg['opencal']['db_path']
        self.opencal_db_path = opencal.path.expand_path(self.opencal_db_path)
        self.con = sqlite3.connect(self.opencal_db_path)
        self.cur = self.con.cursor()
    
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

    @property
    def remaining_cards(self):
        return float("inf")      # Some professor may ask the same questions for an infinite (or unpredictable) number of times

    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        raise NotImplementedError()
    
    ###################################

    def save_current_card_reply(self, review_duration_ms, is_right_answer):
        """Save the reply in the database"""

        card_id = 0    # TODO... SQL SELECT...

        sql_request_values_dict = {
            "card_id": card_id,
            "review_datetime": datetime.datetime.now(),
            "review_duration_ms": review_duration_ms,
            "is_right_answer": is_right_answer
        }

        sql_request = f"""INSERT INTO {ITM_REVIEW_TABLE_NAME}
        ( card_id,  review_datetime,  review_duration_ms,  is_right_answer) VALUES
        (:card_id, :review_datetime, :review_duration_ms, :is_right_answer)
        """

        # This is the qmark style:
        self.cur.execute(sql_request, sql_request_values_dict)
        self.con.commit()
