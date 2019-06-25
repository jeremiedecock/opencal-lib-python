"""Ben is a little more professional than Alan.
He doesn't validate reviews when it's too early...
but he doesn't care about late.
"""

import copy
import datetime
import math

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

GRADE_CARD_NEVER_REVIEWED = -1
GRADE_CARD_WRONG_YESTERDAY = -2
GRADE_DONT_REVIEW_THIS_CARD_TODAY = -3

class ProfessorBen:

    def __init__(self, card_list):
        self._card_list = []

        for card in card_list:
            if not card["hidden"]:
                grade = assess(card)
                card["grade"] = grade

                if grade != GRADE_DONT_REVIEW_THIS_CARD_TODAY:
                    self._card_list.append(card)

        self._card_list.sort(key=lambda _card : _card["grade"])

    @property
    def current_card(self):
        return self._card_list[0] if len(self._card_list) > 0 else None

    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        if len(self._card_list) > 0:
            card = self._card_list.pop(0)

            if answer == "skip":
                if not hide:
                    self._card_list.append(card)
            elif answer == RIGHT_ANSWER_STR:
                review = {
                    "rdate": datetime.datetime.now().date(),
                    "result": RIGHT_ANSWER_STR
                }
                card["reviews"].append(review)
            elif answer == WRONG_ANSWER_STR:
                review = {
                    "rdate": datetime.datetime.now().date(),
                    "result": WRONG_ANSWER_STR
                }
                card["reviews"].append(review)
            else:
                raise ValueError("Unknown answer : {}".format(answer))

            if hide:
                card["hidden"] = True


def datetime_to_date(d):
    '''If the object is an instance of datetime.datetime then convert it to a datetime.datetime.date object.

    If it's already a date object, do nothing.'''

    if isinstance(d, datetime.datetime):
        d = d.date()
    return d


def assess(card, today=None):
    grade = 0

    cdate = datetime_to_date(card["cdate"])

    if today is None:
        today = datetime.datetime.now().date()
    today = datetime_to_date(today)

    if "reviews" in card.keys() and len(card["reviews"]) > 0:
        # There is at least one review

        review_list = card["reviews"]

        # Reviews are supposed to be sorted!
        assert all(review_list[i]["rdate"] <= review_list[i+1]["rdate"] for i in range(len(review_list)-1))
        #review_list.sort(key=lambda x: x["rdate"])

        yesterday = today - datetime.timedelta(days=1)
        last_review_result = review_list[-1]["result"]
        last_review_rdate = datetime_to_date(review_list[-1]["rdate"])
        if last_review_result == WRONG_ANSWER_STR and last_review_rdate == yesterday:
            grade = GRADE_CARD_WRONG_YESTERDAY
        else:
            expected_revision_date = get_expected_revision_date(cdate, grade)

            for review in review_list:
                rdate = datetime_to_date(review["rdate"])
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
                grade = GRADE_DONT_REVIEW_THIS_CARD_TODAY
    else:
        expected_revision_date = get_expected_revision_date(cdate, grade)

        if expected_revision_date > today:
            grade = GRADE_DONT_REVIEW_THIS_CARD_TODAY
        else:
            grade = GRADE_CARD_NEVER_REVIEWED

    return grade


def get_expected_revision_date(last_revision_date, grade):
    """Get the expected (next) revision date knowing the last revision date and the grade."""
    return last_revision_date + datetime.timedelta(days=delta_days(grade))

     
def delta_days(grade):
    """Return the delta day (time between expectedRevisionDate and rdate) knowing the grade.
    
    delta = 2^grade.
    """
    return int(math.pow(2, grade))