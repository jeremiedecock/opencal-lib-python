"""Ben is a little more professional than Alan.
He doesn't validate reviews when it's too early...
but he doesn't care about late.
"""

import copy
import datetime
import math

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

DONT_REVIEW_THIS_TODAY = -1
HAS_NEVER_BEEN_REVIEWED = 0

class ProfessorBen:

    def __init__(self, card_list):
        self._card_list = card_list
        self._current_card_index = 0
    
    @property
    def current_card(self):
        return self._card_list[self._current_card_index]
    
    def current_card_reply(self, answer, duration=None, confidence=None):
        self._current_card_index += 1       # TODO


def assess(card, today=None):
    grade = 0

    if "reviews" in card.keys():
        # There is at least one review

        review_list = card["reviews"]

        cdate = card["cdate"]
        expected_revision_date = get_expected_revision_date(cdate, grade)

        # Reviews are supposed to be sorted!
        assert all(review_list[i]["rdate"] <= review_list[i+1]["rdate"] for i in range(len(review_list)-1))
        #review_list.sort(key=lambda x: x["rdate"])

        if today is None:
            today = datetime.datetime.now().date()
        
        for review in review_list:
            rdate = review["rdate"]
            result = review["result"]

            if rdate <= today:                            # Ignore future reviews
                if result == RIGHT_ANSWER_STR:
                    if rdate >= expected_revision_date:   # "rdate before expected_revision_date"
                        grade += 1
                        expected_revision_date = get_expected_revision_date(rdate, grade)
                else:
                    grade = 0
                    expected_revision_date = get_expected_revision_date(rdate, grade)
        
        if expected_revision_date > today:            # "today before expected_revision_date"
            # It's too early to review this card. The card will be hide
            grade = DONT_REVIEW_THIS_TODAY
    else:
        grade = HAS_NEVER_BEEN_REVIEWED

    return grade


def get_expected_revision_date(last_revision_date, grade):
    """Get the expected (next) revision date knowing the last revision date and the grade."""
    return last_revision_date + datetime.timedelta(days=delta_days(grade))

     
def delta_days(grade):
    """Return the delta day (time between expectedRevisionDate and rdate) knowing the grade.
    
    delta = 2^grade.
    """
    return int(math.pow(2, grade))