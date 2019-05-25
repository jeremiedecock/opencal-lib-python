"""Ben is a little more professional than Alan.
He doesn't validate reviews when it's too early...
but he doesn't care about late.
"""

import copy
import datetime
import math

RIGHT_ANSWER_STR = "good"
WRONG_ANSWER_STR = "wrong"

DONT_REVIEW_THIS_TODAY = -1
HAS_NEVER_BEEN_REVIEWED = 0

def assess(card, today=None):
    grade = 0

    if "reviews" in card.keys():
        # There is at least one review

        review_list = card["reviews"]

        cdate = card["cdate"]
        expected_revision_date = get_expected_revision_date(cdate, grade)

        # TODO: sort reviews

        for review in review_list:
            rdate = review["rdate"]
            result = review["result"]

            if result == RIGHT_ANSWER_STR:
                if rdate >= expected_revision_date:   # "rdate before expected_revision_date"
                    grade += 1
                    expected_revision_date = get_expected_revision_date(rdate, grade)
            else:
                grade = 0
                expected_revision_date = get_expected_revision_date(rdate, grade)
        
        if today is None:
            today = datetime.datetime.now().date()
        
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