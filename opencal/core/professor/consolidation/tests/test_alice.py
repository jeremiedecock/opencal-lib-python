#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.core.professor.consolidation.alice" module.
"""

from opencal.card import Card
from opencal.core.professor.consolidation import alice

from opencal.core.mocks import DateMock

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

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
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_MADE_TODAY = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_MADE_TODAY_WITH_TIME = {
        "cdate": datetime.datetime(year=2000, month=1, day=1, hour=0, minute=1),
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_MADE_YESTERDAY_WITH_TIME = {
        "cdate": datetime.datetime(year=1999, month=12, day=31, hour=23, minute=59),
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_BASIC_LEVEL_MINUS1_1 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
            'reviews': [],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_BASIC_LEVEL_MINUS1_2 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
            'reviews': [],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_BASIC_LEVEL0_1 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                    "result": WRONG_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_BASIC_LEVEL0_2 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                    "result": RIGHT_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_BASIC_LEVEL1_1 = {
        'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        'reviews': [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                "result": RIGHT_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_BASIC_LEVEL2_1 = {
        'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        'reviews': [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
                "result": RIGHT_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_BASIC_LEVEL2_2 = {
        'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=11),
        'reviews': [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                "result": RIGHT_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_BASIC_LEVEL2_3 = {
        'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=17),
        'reviews': [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=15),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=12),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": WRONG_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                "result": RIGHT_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_REVIEWS_NOT_SORTED = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": WRONG_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_IGNORE_PREMATURE_RIGHT_REVIEWS = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8), # <- Too early and as it's a "right" answer, it should be ignored.
                "result": RIGHT_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_IGNORE_PREMATURE_BAD_REVIEWS = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8), # <- Too early, but as it's a WRONG_ANSWER_STR answer, it should *not* be ignored.
                "result": WRONG_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_IGNORE_PREMATURE_BAD_REVIEWS_YESTERDAY = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1), # <- Too early, but as it's a WRONG_ANSWER_STR answer, it should *not* be ignored.
                "result": WRONG_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_IGNORE_FUTURE_REVIEWS = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=12),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE + datetime.timedelta(days=1),
                "result": WRONG_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_WRONG_REVIEW_YESTERDAY = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
                "result": WRONG_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_NOT_TO_BE_REVIEWED_TODAY = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
                "result": RIGHT_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_WRONG_REVIEW_TODAY = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                "result": RIGHT_ANSWER_STR
            },
            {
                "rdate": BOGUS_CURRENT_DATE,
                "result": WRONG_ANSWER_STR
            }
        ],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
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
    assert alice.assess(CARD_WITHOUT_REVIEW, DateMock) == alice.GRADE_CARD_NEVER_REVIEWED
    assert alice.assess(CARD_BASIC_LEVEL_MINUS1_1, DateMock) == alice.GRADE_CARD_NEVER_REVIEWED
    assert alice.assess(CARD_BASIC_LEVEL_MINUS1_2, DateMock) == alice.GRADE_CARD_NEVER_REVIEWED

def test_card_made_today():
    assert alice.assess(CARD_MADE_TODAY, DateMock) == alice.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_today_with_time():
    assert alice.assess(CARD_MADE_TODAY_WITH_TIME, DateMock) == alice.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_yesterday_with_time():
    assert alice.assess(CARD_MADE_YESTERDAY_WITH_TIME, DateMock) == alice.GRADE_CARD_NEVER_REVIEWED

def test_basic_cards():
    assert alice.assess(CARD_BASIC_LEVEL0_1, DateMock) == 0
    assert alice.assess(CARD_BASIC_LEVEL0_2, DateMock) == 0
    assert alice.assess(CARD_BASIC_LEVEL1_1, DateMock) == 1
    assert alice.assess(CARD_BASIC_LEVEL2_1, DateMock) == 2
    assert alice.assess(CARD_BASIC_LEVEL2_2, DateMock) == 2
    assert alice.assess(CARD_BASIC_LEVEL2_3, DateMock) == 2

def test_reviews_not_sorted():
    #assert alice.assess(CARD_REVIEWS_NOT_SORTED, BOGUS_CURRENT_DATE) == 2
    with pytest.raises(AssertionError):
        alice.assess(CARD_REVIEWS_NOT_SORTED, DateMock)

def test_ignore_premature_right_reviews():
    assert alice.assess(CARD_IGNORE_PREMATURE_RIGHT_REVIEWS, DateMock) == 1

def test_ignore_premature_bad_reviews():
    assert alice.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS, DateMock) == 0

def test_ignore_premature_bad_reviews_yesterday():
    assert alice.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS_YESTERDAY, DateMock) == alice.GRADE_CARD_WRONG_YESTERDAY

def test_ignore_future_reviews():
    assert alice.assess(CARD_IGNORE_FUTURE_REVIEWS, DateMock) == 2

def test_card_wrong_review_yesterday():
    assert alice.assess(CARD_WRONG_REVIEW_YESTERDAY, DateMock) == alice.GRADE_CARD_WRONG_YESTERDAY

def test_card_wrong_review_today():
    assert alice.assess(CARD_WRONG_REVIEW_TODAY, DateMock) == alice.GRADE_DONT_REVIEW_THIS_CARD_TODAY
    assert alice.assess(CARD_NOT_TO_BE_REVIEWED_TODAY, DateMock) == alice.GRADE_DONT_REVIEW_THIS_CARD_TODAY


###############################################################################
# TEST THE PROFESSOR'S CONSTRUCTOR,                                           #
# PLUS THE "current_card" AND "current_card_reply" METHODS                    #
###############################################################################

def test_empty_card_list():
    """Test `professor.current_card`.

    Check that `professor.current_card` returns `None` on empty card lists.
    """
    prof = alice.ProfessorAlice(EMPTY_CARD_LIST)
    assert prof.current_card == None

def test_one_card_right():
    """Test `professor.current_card` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer="skip")` puts the card back at the
      end of the stack ;
    - `professor.current_card_reply(answer=RIGHT_ANSWER_STR)` remove the card from the
      stack and add the right "review" item to the card ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_1 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = alice.ProfessorAlice([card_1], date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    assert card_1["reviews"][-1]['rdate'] == BOGUS_CURRENT_DATE
    assert card_1["reviews"][-1]['result'] == RIGHT_ANSWER_STR

    current_card = prof.current_card
    assert current_card == None

def test_one_card_wrong():
    """Test `professor.current_card` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer="skip")` puts the card back at the
      end of the stack ;
    - `professor.current_card_reply(answer="wrong")` remove the card from the
      stack and add the right "review" item to the card ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_1 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = alice.ProfessorAlice([card_1], date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer=WRONG_ANSWER_STR)

    assert card_1["reviews"][-1]['rdate'] == BOGUS_CURRENT_DATE
    assert card_1["reviews"][-1]['result'] == WRONG_ANSWER_STR

    current_card = prof.current_card
    assert current_card == None

def test_right_wrong_and_hide_reply():
    """Test `professor.current_card` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer=RIGHT_ANSWER_STR, hide=True)` remove
      the card from the stack and add the right "review" item to the card and
      hide the card ;
    - `professor.current_card_reply(answer=WRONG_ANSWER_STR, hide=True)` remove
      the card from the stack and add the right "review" item to the card and
      hide the card ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = alice.ProfessorAlice([card_level0_age5, card_level0_age4],
                                date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_level0_age5
    prof.current_card_reply(answer=RIGHT_ANSWER_STR, hide=True)

    assert card_level0_age5["reviews"][-1]['rdate'] == BOGUS_CURRENT_DATE
    assert card_level0_age5["reviews"][-1]['result'] == RIGHT_ANSWER_STR
    assert card_level0_age5['hidden'] == True

    current_card = prof.current_card
    assert current_card == card_level0_age4
    prof.current_card_reply(answer=WRONG_ANSWER_STR, hide=True)

    assert card_level0_age4["reviews"][-1]['rdate'] == BOGUS_CURRENT_DATE
    assert card_level0_age4["reviews"][-1]['result'] == WRONG_ANSWER_STR
    assert card_level0_age4['hidden'] == True

    current_card = prof.current_card
    assert current_card == None

def test_hide_cards():
    """Test `professor.current_card` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer="skip", hide=True)` remove
      the card from the stack and hide the card without adding any review item;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = alice.ProfessorAlice([card_level0_age5, card_level0_age4],
                                date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_level0_age5
    prof.current_card_reply(answer="skip", hide=True)

    assert len(card_level0_age5["reviews"]) == len(CARD_BASIC_LEVEL0_2["reviews"])
    assert card_level0_age5['hidden'] == True

    current_card = prof.current_card
    assert current_card == card_level0_age4
    prof.current_card_reply(answer="skip", hide=True)

    assert len(card_level0_age4["reviews"]) == len(CARD_BASIC_LEVEL0_1["reviews"])
    assert card_level0_age4['hidden'] == True

    current_card = prof.current_card
    assert current_card == None

def test_one_hidden_card():
    """Test `professor.current_card` and `professor.current_card_reply()`.

    Check that:
    - `professor` exclude hidden cards ;
    - `professor.current_card` returns `None` when card lists contains hidden
      cards only.
    """
    prof = alice.ProfessorAlice(copy.deepcopy(ONE_HIDDEN_CARD))
    assert prof.current_card == None

def test_three_cards_two_hidden():
    """Test `professor.current_card` and `professor.current_card_reply()`.

    Check that:
    - `professor` exclude hidden cards ;
    - `professor.current_card_reply(answer="skip")` puts the card back at the
      end of the stack ;
    - `professor.current_card` returns `None` when card lists contains hidden
      cards only.
    """
    card_1 = copy.deepcopy(CARD_HIDDEN)
    card_2 = copy.deepcopy(CARD_BASIC_LEVEL2_1)
    card_3 = copy.deepcopy(CARD_HIDDEN)

    prof = alice.ProfessorAlice([card_1, card_2, card_3],
                                date_mock=DateMock)
    
    current_card = prof.current_card
    assert current_card == card_2
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_2
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == None

def test_several_cards():
    """Test `professor.current_card` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card` returns the expected cards ;
    - `professor` sort well cards: first `GRADE_CARD_WRONG_YESTERDAY` then
      `GRADE_CARD_NEVER_REVIEWED` then cards having grade 0 (cards that have
      never been reviewed and that have been created more than one day ago);
    - `professor` exclude cards that have been created today;
    - `professor` exclude cards that don't have to be reviewed today;
    - `professor` ignore wrong dates (future dates);
    - `professor` ignore wrong dates (future dates);
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_hidden_age1 = copy.deepcopy(CARD_HIDDEN)

    card_level_min3_age8 = copy.deepcopy(CARD_WRONG_REVIEW_TODAY)
    card_level_min3_age4 = copy.deepcopy(CARD_NOT_TO_BE_REVIEWED_TODAY)
    card_level_min3_age0 = copy.deepcopy(CARD_MADE_TODAY)

    card_level_min2_age8 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY)

    card_level_min1_age1 = copy.deepcopy(CARD_WITHOUT_REVIEW)
    
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)
    
    card_level1_age10 = copy.deepcopy(CARD_BASIC_LEVEL1_1)

    card_level2_age17 = copy.deepcopy(CARD_BASIC_LEVEL2_3)
    card_level2_age12 = copy.deepcopy(CARD_IGNORE_FUTURE_REVIEWS)
    card_level2_age11 = copy.deepcopy(CARD_BASIC_LEVEL2_2)
    card_level2_age10 = copy.deepcopy(CARD_BASIC_LEVEL2_1)

    card_list = [
            card_level2_age17,
            card_level2_age12,
            card_level2_age11,
            card_level2_age10,
            card_level1_age10,
            card_level_min3_age8,
            card_level_min2_age8,
            card_level_min3_age4,
            card_level0_age5,
            card_level0_age4,
            card_hidden_age1,
            card_level_min1_age1,
            card_level_min3_age0,
        ]
    
    prof = alice.ProfessorAlice(card_list,
                                date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_level_min2_age8
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level_min1_age1
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level0_age5
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_level0_age4
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level1_age10
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level2_age17
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level2_age12
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level2_age11
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level2_age10
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == card_level0_age5
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == None
