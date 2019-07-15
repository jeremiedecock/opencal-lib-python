#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.core.professor.ben" module.
"""

from opencal.core.professor import ben

from opencal.core.mocks import DateMock

import copy
import datetime
import pytest

BOGUS_CURRENT_DATE = datetime.date(year=2000, month=1, day=1)

DateMock.set_today(BOGUS_CURRENT_DATE)

###############################################################################
# CARDS                                                                       #
###############################################################################

CARD_WITHOUT_REVIEW = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
        "reviews": []
    }

CARD_WITHOUT_REVIEW_2 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1)
    }

CARD_MADE_TODAY = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": []
    }

CARD_MADE_TODAY_2 = {
        "cdate": BOGUS_CURRENT_DATE
    }

CARD_MADE_TODAY_WITH_TIME = {
        "cdate": datetime.datetime(year=2000, month=1, day=1, hour=0, minute=1),
        "reviews": []
    }

CARD_MADE_YESTERDAY_WITH_TIME = {
        "cdate": datetime.datetime(year=1999, month=12, day=31, hour=23, minute=59),
        "reviews": []
    }

CARD_BASIC_1 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": "bad"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
                "result": "good"
            }
        ]
    }

CARD_BASIC_2 = {
            'reviews': [],
            'tags': ['baz'],
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_BASIC_3 = {
            'reviews': [],
            'tags': ['baz'],
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_REVIEWS_NOT_SORTED = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": "bad"
            }
        ]
    }

CARD_IGNORE_PREMATURE_RIGHT_REVIEWS = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8), # <- Too early and as it's a "right" answer, it should be ignored.
                "result": "good"
            }
        ]
    }

CARD_IGNORE_PREMATURE_BAD_REVIEWS = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8), # <- Too early, but as it's a "bad" answer, it should *not* be ignored.
                "result": "bad"
            }
        ]
    }

CARD_IGNORE_PREMATURE_BAD_REVIEWS_YESTERDAY = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1), # <- Too early, but as it's a "bad" answer, it should *not* be ignored.
                "result": "bad"
            }
        ]
    }

CARD_IGNORE_FUTURE_REVIEWS = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE + datetime.timedelta(days=1),
                "result": "bad"
            }
        ]
    }

CARD_WRONG_REVIEW_YESTERDAY = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
                "result": "bad"
            }
        ]
    }

CARD_WRONG_REVIEW_TODAY = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                "result": "good"
            },
            {
                "rdate": BOGUS_CURRENT_DATE,
                "result": "bad"
            }
        ]
    }

CARD_HIDDEN = {
            'reviews': [],
            'tags': ['baz'],
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
            'hidden': True,
            'question': 'foo',
            'answer': 'bar'
        }


###############################################################################
# CARD LISTS                                                                  #
###############################################################################

EMPTY_CARD_LIST = []

ONE_HIDDEN_CARD = [CARD_HIDDEN]


###############################################################################
# TEST THE "assess" FUNCTION                                                  #
###############################################################################

def test_card_without_review():
    assert ben.assess(CARD_WITHOUT_REVIEW, DateMock) == ben.GRADE_CARD_NEVER_REVIEWED

def test_card_without_review_2():
    assert ben.assess(CARD_WITHOUT_REVIEW_2, DateMock) == ben.GRADE_CARD_NEVER_REVIEWED

def test_card_made_today():
    assert ben.assess(CARD_MADE_TODAY, DateMock) == ben.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_today_with_time():
    assert ben.assess(CARD_MADE_TODAY_WITH_TIME, DateMock) == ben.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_yesterday_with_time():
    assert ben.assess(CARD_MADE_YESTERDAY_WITH_TIME, DateMock) == ben.GRADE_CARD_NEVER_REVIEWED

def test_card_made_today_2():
    assert ben.assess(CARD_MADE_TODAY_2, DateMock) == ben.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_basic_card():
    assert ben.assess(CARD_BASIC_1, DateMock) == 2

def test_reviews_not_sorted():
    #assert ben.assess(CARD_REVIEWS_NOT_SORTED, BOGUS_CURRENT_DATE) == 2
    with pytest.raises(AssertionError):
        ben.assess(CARD_REVIEWS_NOT_SORTED, DateMock)

def test_ignore_premature_right_reviews():
    assert ben.assess(CARD_IGNORE_PREMATURE_RIGHT_REVIEWS, DateMock) == 1

def test_ignore_premature_bad_reviews():
    assert ben.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS, DateMock) == 0

def test_ignore_premature_bad_reviews_yesterday():
    assert ben.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS_YESTERDAY, DateMock) == ben.GRADE_CARD_WRONG_YESTERDAY

def test_ignore_future_reviews():
    assert ben.assess(CARD_IGNORE_FUTURE_REVIEWS, DateMock) == 2

def test_card_wrong_review_yesterday():
    assert ben.assess(CARD_WRONG_REVIEW_YESTERDAY, DateMock) == ben.GRADE_CARD_WRONG_YESTERDAY

def test_card_wrong_review_today():
    assert ben.assess(CARD_WRONG_REVIEW_TODAY, DateMock) == ben.GRADE_DONT_REVIEW_THIS_CARD_TODAY


###############################################################################
# TEST THE "current_card" AND "current_card_reply" FUNCTIONS                  #
###############################################################################

def test_empty_card_list():
    prof = ben.ProfessorBen(EMPTY_CARD_LIST)
    assert prof.current_card == None

def test_one_card_right():
    card_1 = copy.deepcopy(CARD_BASIC_2)

    prof = ben.ProfessorBen([card_1], date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="good")

    current_card = prof.current_card
    assert current_card == None

def test_one_card_wrong():
    card_1 = copy.deepcopy(CARD_BASIC_2)

    prof = ben.ProfessorBen([card_1], date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="bad")

    current_card = prof.current_card
    assert current_card == None

def test_one_hidden_card():
    prof = ben.ProfessorBen(copy.deepcopy(ONE_HIDDEN_CARD))
    assert prof.current_card == None

def test_several_cards():
    card_1 = copy.deepcopy(CARD_BASIC_2)
    card_2 = copy.deepcopy(CARD_BASIC_3)

    prof = ben.ProfessorBen([card_1, card_2],
                            date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_2
    prof.current_card_reply(answer="bad")

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="good")

    current_card = prof.current_card
    assert current_card == None