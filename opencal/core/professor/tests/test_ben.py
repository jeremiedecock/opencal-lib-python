#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.core.professor.ben" module.
"""

import opencal.core.professor.ben as prof

from opencal.core.mocks import DateMock

import datetime
import pytest

BOGUS_CURRENT_DATE = datetime.date(year=2000, month=1, day=1)

DateMock.set_today(BOGUS_CURRENT_DATE)

# Test the "assess" function ##################################################

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

CARD_BASIC = {
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

def test_card_without_review():
    assert prof.assess(CARD_WITHOUT_REVIEW, DateMock) == prof.GRADE_CARD_NEVER_REVIEWED

def test_card_without_review_2():
    assert prof.assess(CARD_WITHOUT_REVIEW_2, DateMock) == prof.GRADE_CARD_NEVER_REVIEWED

def test_card_made_today():
    assert prof.assess(CARD_MADE_TODAY, DateMock) == prof.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_today_with_time():
    assert prof.assess(CARD_MADE_TODAY_WITH_TIME, DateMock) == prof.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_yesterday_with_time():
    assert prof.assess(CARD_MADE_YESTERDAY_WITH_TIME, DateMock) == prof.GRADE_CARD_NEVER_REVIEWED

def test_card_made_today_2():
    assert prof.assess(CARD_MADE_TODAY_2, DateMock) == prof.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_basic_card():
    assert prof.assess(CARD_BASIC, DateMock) == 2

def test_reviews_not_sorted():
    #assert prof.assess(CARD_REVIEWS_NOT_SORTED, BOGUS_CURRENT_DATE) == 2
    with pytest.raises(AssertionError):
        prof.assess(CARD_REVIEWS_NOT_SORTED, DateMock)

def test_ignore_premature_right_reviews():
    assert prof.assess(CARD_IGNORE_PREMATURE_RIGHT_REVIEWS, DateMock) == 1

def test_ignore_premature_bad_reviews():
    assert prof.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS, DateMock) == 0

def test_ignore_premature_bad_reviews_yesterday():
    assert prof.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS_YESTERDAY, DateMock) == prof.GRADE_CARD_WRONG_YESTERDAY

def test_ignore_future_reviews():
    assert prof.assess(CARD_IGNORE_FUTURE_REVIEWS, DateMock) == 2

def test_card_wrong_review_yesterday():
    assert prof.assess(CARD_WRONG_REVIEW_YESTERDAY, DateMock) == prof.GRADE_CARD_WRONG_YESTERDAY

def test_card_wrong_review_today():
    assert prof.assess(CARD_WRONG_REVIEW_TODAY, DateMock) == prof.GRADE_DONT_REVIEW_THIS_CARD_TODAY