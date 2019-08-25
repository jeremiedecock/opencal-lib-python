"""Berenice is the second professor implemented for long-term memory training in OpenCAL."""

import copy
import datetime
import math

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

GRADE_CARD_NEVER_REVIEWED = -1
GRADE_CARD_WRONG_YESTERDAY = -2
GRADE_DONT_REVIEW_THIS_CARD_TODAY = -3

class ProfessorBerenice:

    def __init__(self, card_list, date_mock=None):
        self._card_list_dict = {}

        if date_mock is None:
            self._date = datetime.date
        else:
            self._date = date_mock

        for card in card_list:
            if not card["hidden"]:
                grade = assess(card, date_mock=date_mock)
                card["grade"] = grade

                if grade != GRADE_DONT_REVIEW_THIS_CARD_TODAY:
                    if grade not in self._card_list_dict:
                        self._card_list_dict[grade] = []
                    self._card_list_dict[grade].append(card)

        self.switch_grade()


    def switch_grade(self):
        if len(self._card_list_dict.keys()) > 0:
            self.current_grade = sorted(self._card_list_dict.keys())[0]
            self.current_sub_list = self._card_list_dict.pop(self.current_grade)  # rem: this remove current_grade from _card_list_dict

            # TODO: estimate the priority of each card... -> utilise deux liste de liste tags definie dans le fichier de config .yaml : prof_berenice_high_priority_tags = [['maths', 'algebre', ...], ['accenta'], ['important', 'high priority', ...], ...] ; prof_berebice_low_priority_tags = [[...], ...] -> chaque sous liste est un ensemble de tags équivalant ; chaque tag ds high priority => card priority += 1 ; chaque tag dans low_prio_list => card priority -= 1
            # TODO: sort current_sub_list according to the priority level of each card
            #self.current_sub_list.sort(key=lambda _card : _card["grade"])
        else:
            self.current_grade = None
            self.current_sub_list = None

        self.num_right_answer_current_grade = 0


    @property
    def current_card(self):
        if self.current_sub_list is not None:
            if len(self.current_sub_list) == 0: # TODO: or self.num_right_answer_current_grade >= NUM_CARDS_PER_GRADE
                self.switch_grade()

        return self.current_sub_list[0] if self.current_sub_list is not None else None


    def current_card_reply(self, answer, hide=False, duration=None, confidence=None):
        if len(self.current_sub_list) > 0:
            card = self.current_sub_list.pop(0)

            if answer == RIGHT_ANSWER_STR:
                review = {
                    "rdate": self._date.today(),
                    "result": RIGHT_ANSWER_STR
                }
                card["reviews"].append(review)
                self.num_right_answer_current_grade += 1
            elif answer == WRONG_ANSWER_STR:
                review = {
                    "rdate": self._date.today(),
                    "result": WRONG_ANSWER_STR
                }
                card["reviews"].append(review)
            elif answer == "skip":
                pass
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


def assess(card, date_mock=None):
    grade = 0

    cdate = datetime_to_date(card["cdate"])

    if date_mock is None:
        today = datetime.date.today()
    else:
        today = date_mock.today()

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
