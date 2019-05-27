#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.core.professor.ben" module.
"""

import opencal.core.professor.ben as prof

import datetime
import numpy as np
import os
import pytest
import tempfile

# Test the "load_pkb" and "save_pkb" functions ################################

BOGUS_CURRENT_DATE = datetime.datetime(year=2000, month=1, day=1).date()

CARD_WITHOUT_REVIEW = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
        "reviews": []
    }

CARD_MADE_TODAY = {
        "cdate": BOGUS_CURRENT_DATE,
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

def test_card_without_review():
    assert prof.assess(CARD_WITHOUT_REVIEW, BOGUS_CURRENT_DATE) == prof.HAS_NEVER_BEEN_REVIEWED

def test_card_made_today():
    assert prof.assess(CARD_MADE_TODAY, BOGUS_CURRENT_DATE) == prof.DONT_REVIEW_THIS_TODAY

def test_basic_card():
    assert prof.assess(CARD_BASIC, BOGUS_CURRENT_DATE) == 2

def test_reviews_not_sorted():
    #assert prof.assess(CARD_REVIEWS_NOT_SORTED, BOGUS_CURRENT_DATE) == 2
    with pytest.raises(AssertionError):
        prof.assess(CARD_REVIEWS_NOT_SORTED, BOGUS_CURRENT_DATE)