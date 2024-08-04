#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.core.professor.acquisition.randy" module.
"""

from opencal.core.professor.acquisition import randy

import datetime
import random

# CARDS ###################################################

CARD_1 = {
            'reviews': [],
            'tags': ['baz'],
            'cdate': datetime.datetime(2018, 1, 1, 0, 0),
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_2 = {
            'reviews': [],
            'tags': ['baz'],
            'cdate': datetime.datetime(2018, 1, 2, 0, 0),
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

HIDDEN_CARD_1 = {
            'reviews': [],
            'tags': ['baz'],
            'cdate': datetime.datetime(2018, 1, 1, 0, 0),
            'hidden': True,
            'question': 'foo',
            'answer': 'bar'
        }

# CARD LISTS ##############################################

EMPTY_CARD_LIST = []

ONE_CARD = [CARD_1]

ONE_HIDDEN_CARD = [HIDDEN_CARD_1]

SEVERAL_CARDS = [CARD_1, CARD_2]

# TEST FUNCTIONS ##########################################

def test_empty_card_list():
    prof = randy.ProfessorRandy(EMPTY_CARD_LIST)
    assert prof.current_card == None

def test_one_card():
    prof = randy.ProfessorRandy(ONE_CARD)

    current_card = prof.current_card
    assert current_card == CARD_1
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == CARD_1
    prof.current_card_reply(answer="bad")

    current_card = prof.current_card
    assert current_card == CARD_1
    prof.current_card_reply(answer="good")

    current_card = prof.current_card
    assert current_card == None

def test_one_hidden_card():
    prof = randy.ProfessorRandy(ONE_HIDDEN_CARD)
    assert prof.current_card == None

def test_several_cards():
    random.seed(1)

    prof = randy.ProfessorRandy(SEVERAL_CARDS)

    current_card = prof.current_card
    assert current_card == CARD_2
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == CARD_1
    prof.current_card_reply(answer="bad")

    current_card = prof.current_card
    assert current_card == CARD_2
    prof.current_card_reply(answer="good")

    current_card = prof.current_card
    assert current_card == CARD_1
    prof.current_card_reply(answer="good")

    current_card = prof.current_card
    assert current_card == None
