#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.core.professor.consolidation.doreen" module.
"""

from opencal.card import Card
from opencal.core.professor.consolidation import doreen

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

CARD_WITHOUT_REVIEW_1 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_WITHOUT_REVIEW_2 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
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

CARD_REVIEWED_TODAY_1 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE,
                    "result": RIGHT_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_REVIEWED_TODAY_2 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE,
                    "result": RIGHT_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_REVIEWED_TODAY_3 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE,
                    "result": WRONG_ANSWER_STR
                }
            ],
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

CARD_BASIC_LEVEL0_3 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                    "result": WRONG_ANSWER_STR
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

CARD_BASIC_LEVEL0_4 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_BASIC_LEVEL0_5 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=7),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_BASIC_LEVEL0_6 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
            'reviews': [
                {
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
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
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

CARD_WRONG_REVIEW_YESTERDAY_1 = {
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

CARD_WRONG_REVIEW_YESTERDAY_2 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
        "reviews": [
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

CARD_WRONG_REVIEW_YESTERDAY_3 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
        "reviews": [
            {
                "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                "result": WRONG_ANSWER_STR
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
    assert doreen.assess(CARD_WITHOUT_REVIEW_1, DateMock) == 0
    assert doreen.assess(CARD_BASIC_LEVEL_MINUS1_1, DateMock) == 0
    assert doreen.assess(CARD_BASIC_LEVEL_MINUS1_2, DateMock) == 0

def test_card_made_today():
    assert doreen.assess(CARD_MADE_TODAY, DateMock) == doreen.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_today_with_time():
    assert doreen.assess(CARD_MADE_TODAY_WITH_TIME, DateMock) == doreen.GRADE_DONT_REVIEW_THIS_CARD_TODAY

def test_card_made_yesterday_with_time():
    assert doreen.assess(CARD_MADE_YESTERDAY_WITH_TIME, DateMock) == 0

def test_basic_cards():
    assert doreen.assess(CARD_BASIC_LEVEL0_1, DateMock) == 0
    assert doreen.assess(CARD_BASIC_LEVEL0_2, DateMock) == 0
    assert doreen.assess(CARD_BASIC_LEVEL1_1, DateMock) == 1
    assert doreen.assess(CARD_BASIC_LEVEL2_1, DateMock) == 2
    assert doreen.assess(CARD_BASIC_LEVEL2_2, DateMock) == 2
    assert doreen.assess(CARD_BASIC_LEVEL2_3, DateMock) == 2

def test_reviews_not_sorted():
    #assert doreen.assess(CARD_REVIEWS_NOT_SORTED, BOGUS_CURRENT_DATE) == 2
    with pytest.raises(AssertionError):
        doreen.assess(CARD_REVIEWS_NOT_SORTED, DateMock)

def test_ignore_premature_right_reviews():
    assert doreen.assess(CARD_IGNORE_PREMATURE_RIGHT_REVIEWS, DateMock) == 1

def test_ignore_premature_bad_reviews():
    assert doreen.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS, DateMock) == 0

def test_ignore_premature_bad_reviews_yesterday():
    assert doreen.assess(CARD_IGNORE_PREMATURE_BAD_REVIEWS_YESTERDAY, DateMock) == 0

def test_ignore_future_reviews():
    with pytest.warns(UserWarning):
        assert doreen.assess(CARD_IGNORE_FUTURE_REVIEWS, DateMock) == 2

def test_card_wrong_review_yesterday():
    assert doreen.assess(CARD_WRONG_REVIEW_YESTERDAY_1, DateMock) == 0

def test_card_wrong_review_today():
    assert doreen.assess(CARD_WRONG_REVIEW_TODAY, DateMock) == doreen.GRADE_DONT_REVIEW_THIS_CARD_TODAY
    assert doreen.assess(CARD_NOT_TO_BE_REVIEWED_TODAY, DateMock) == doreen.GRADE_DONT_REVIEW_THIS_CARD_TODAY


###############################################################################
# TEST THE "estimate_card_difficulty" FUNCTION                                #
###############################################################################

TAG_EASY = "easy"
TAG_NEUTRAL = "normal"
TAG_DIFFICULT = "difficult"

POINTS_EASY = 0.5
POINTS_NEUTRAL = 1
POINTS_DIFFICULT = 2

CARD_DIFFICULTY_NONE = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_EASY = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_EASY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_NEUTRAL = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_NEUTRAL],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_DIFFICULT = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_DIFFICULT],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_EASY_NEUTRAL = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_EASY, TAG_NEUTRAL],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_NEUTRAL_EASY = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_NEUTRAL, TAG_EASY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_EASY_DIFFICULT = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_EASY, TAG_DIFFICULT],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_DIFFICULT_EASY = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_DIFFICULT, TAG_EASY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_DIFFICULT_NEUTRAL = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_DIFFICULT, TAG_NEUTRAL],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DIFFICULTY_NEUTRAL_DIFFICULT = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_NEUTRAL, TAG_DIFFICULT],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

def test_estimate_card_difficulty():
    tag_difficulty_dict = {
            TAG_EASY: POINTS_EASY,
            TAG_DIFFICULT: POINTS_DIFFICULT
        }

    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_NONE, tag_difficulty_dict) == POINTS_NEUTRAL
    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_EASY, tag_difficulty_dict) == POINTS_EASY
    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_NEUTRAL, tag_difficulty_dict) == POINTS_NEUTRAL
    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_DIFFICULT, tag_difficulty_dict) == POINTS_DIFFICULT
    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_EASY_DIFFICULT, tag_difficulty_dict) == POINTS_DIFFICULT
    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_DIFFICULT_EASY, tag_difficulty_dict) == POINTS_DIFFICULT
    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_DIFFICULT_NEUTRAL, tag_difficulty_dict) == POINTS_DIFFICULT
    assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_NEUTRAL_DIFFICULT, tag_difficulty_dict) == POINTS_DIFFICULT
    #assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_EASY_NEUTRAL, tag_difficulty_dict) == POINTS_EASY
    #assert doreen.estimate_card_difficulty(CARD_DIFFICULTY_NEUTRAL_EASY, tag_difficulty_dict) == POINTS_EASY


###############################################################################
# TEST THE "sort_sub_list" FUNCTION                                           #
###############################################################################

TAG_LOW_PRIORITY = "low priority"
TAG_DEFAULT_PRIORITY = "default priority"
TAG_HIGH_PRIORITY = "high priority"

POINTS_LOW_PRIORITY = -1
POINTS_DEFAULT_PRIORITY = 0
POINTS_HIGH_PRIORITY = 1

CARD_LOW_PRIORITY_C0 = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_LOW_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DEFAULT_PRIORITY_C0 = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_DEFAULT_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_HIGH_PRIORITY_C0 = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': [TAG_HIGH_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_HIGH_PRIORITY_C1 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
        "reviews": [],
        'tags': [TAG_HIGH_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DEFAULT_PRIORITY_C2 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
        "reviews": [],
        'tags': [TAG_DEFAULT_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_HIGH_PRIORITY_C10_R5 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=10),
        'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                    "result": WRONG_ANSWER_STR
                }
            ],
        'tags': [TAG_HIGH_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_LOW_PRIORITY_C15_R2 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=15),
        'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=12),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                }
            ],
        'tags': [TAG_LOW_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_DEFAULT_PRIORITY_C9_R6 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=9),
        'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=8),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
                    "result": WRONG_ANSWER_STR
                }
            ],
        'tags': [TAG_DEFAULT_PRIORITY],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

def test_sort_sub_list():
    tag_priority_dict = {
            TAG_LOW_PRIORITY: POINTS_LOW_PRIORITY,
            TAG_DEFAULT_PRIORITY: POINTS_DEFAULT_PRIORITY,
            TAG_HIGH_PRIORITY: POINTS_HIGH_PRIORITY
        }

    priorities_per_level_dict = {
        0: [
            {'sort_fn': 'tag', 'reverse': True},
            {'sort_fn': 'date', 'reverse': True}
        ],
        'default': [
            {'sort_fn': 'tag', 'reverse': True}
        ]
    }

    # Estimate the priority of each card
    for card in [CARD_LOW_PRIORITY_C0, CARD_DEFAULT_PRIORITY_C0, CARD_HIGH_PRIORITY_C0,
                 CARD_HIGH_PRIORITY_C1, CARD_DEFAULT_PRIORITY_C2,
                 CARD_HIGH_PRIORITY_C10_R5, CARD_LOW_PRIORITY_C15_R2, CARD_DEFAULT_PRIORITY_C9_R6]:
        card["priority"] = doreen.estimate_card_priority(card, tag_priority_dict)
    
    # Check that no exception is raised when sub_list is empty
    doreen.sort_sub_list(sub_list=[], sub_list_grade=0, tag_priority_dict=tag_priority_dict, priorities_per_level=priorities_per_level_dict)

    # Test that card are sorted by descending priority level when sub_list_grade is not zero
    sub_list = [CARD_LOW_PRIORITY_C0, CARD_DEFAULT_PRIORITY_C0, CARD_HIGH_PRIORITY_C0]
    sub_list_grade = 1
    doreen.sort_sub_list(sub_list, sub_list_grade, tag_priority_dict, priorities_per_level=priorities_per_level_dict)
    assert sub_list == [CARD_HIGH_PRIORITY_C0, CARD_DEFAULT_PRIORITY_C0, CARD_LOW_PRIORITY_C0]

    # Test that card are sorted by last update (and by priority when cards have the same last update) when sub_list_grade is zero
    sub_list = [CARD_DEFAULT_PRIORITY_C0, CARD_LOW_PRIORITY_C0, CARD_HIGH_PRIORITY_C0]
    sub_list_grade = 0
    doreen.sort_sub_list(sub_list, sub_list_grade, tag_priority_dict, priorities_per_level=priorities_per_level_dict)
    assert sub_list == [CARD_HIGH_PRIORITY_C0, CARD_DEFAULT_PRIORITY_C0, CARD_LOW_PRIORITY_C0]

    # Test that card are sorted by last update when sub_list_grade is zero
    sub_list = [CARD_LOW_PRIORITY_C0, CARD_DEFAULT_PRIORITY_C2, CARD_HIGH_PRIORITY_C1]
    sub_list_grade = 0
    doreen.sort_sub_list(sub_list, sub_list_grade, tag_priority_dict, priorities_per_level=priorities_per_level_dict)
    assert sub_list == [CARD_LOW_PRIORITY_C0, CARD_HIGH_PRIORITY_C1, CARD_DEFAULT_PRIORITY_C2]

    # Test that card are sorted by last update when sub_list_grade is zero
    sub_list = [CARD_HIGH_PRIORITY_C10_R5, CARD_LOW_PRIORITY_C15_R2, CARD_DEFAULT_PRIORITY_C9_R6]
    sub_list_grade = 0
    doreen.sort_sub_list(sub_list, sub_list_grade, tag_priority_dict, priorities_per_level=priorities_per_level_dict)
    assert sub_list == [CARD_LOW_PRIORITY_C15_R2, CARD_HIGH_PRIORITY_C10_R5, CARD_DEFAULT_PRIORITY_C9_R6]


###############################################################################
# TEST THE PROFESSOR'S CONSTRUCTOR,                                           #
# PLUS THE "current_card" AND "current_card_reply" METHODS                    #
###############################################################################

def test_empty_card_list():
    """Test `professor.current_card` and `professor._switch_grade_loop()`.

    Check that `professor.current_card` returns `None` on empty card lists.
    """
    prof = doreen.ProfessorDoreen(EMPTY_CARD_LIST)
    assert prof.current_card == None

def test_one_card_skip():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer="skip")` removes the card from the stack ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_1 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = doreen.ProfessorDoreen([card_1], date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == None

def test_one_card_right():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer=RIGHT_ANSWER_STR)` remove the card from the
      stack and add the right "review" item to the card ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_1 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = doreen.ProfessorDoreen([card_1], date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    assert card_1["reviews"][-1]['rdate'] == BOGUS_CURRENT_DATE
    assert card_1["reviews"][-1]['result'] == RIGHT_ANSWER_STR

    current_card = prof.current_card
    assert current_card == None

def test_one_card_wrong():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer="wrong")` remove the card from the
      stack and add the right "review" item to the card ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_1 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = doreen.ProfessorDoreen([card_1], date_mock=DateMock)

    current_card = prof.current_card
    assert current_card == card_1
    prof.current_card_reply(answer=WRONG_ANSWER_STR)

    assert card_1["reviews"][-1]['rdate'] == BOGUS_CURRENT_DATE
    assert card_1["reviews"][-1]['result'] == WRONG_ANSWER_STR

    current_card = prof.current_card
    assert current_card == None

def test_right_wrong_and_hide_reply():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

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

    prof = doreen.ProfessorDoreen([card_level0_age5, card_level0_age4],
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
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card_reply(answer="skip", hide=True)` remove
      the card from the stack and hide the card without adding any review item;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)

    prof = doreen.ProfessorDoreen([card_level0_age5, card_level0_age4],
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
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor` exclude hidden cards ;
    - `professor.current_card` returns `None` when card lists contains hidden
      cards only.
    """
    prof = doreen.ProfessorDoreen(copy.deepcopy(ONE_HIDDEN_CARD))
    assert prof.current_card == None

def test_three_cards_two_hidden():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor` exclude hidden cards ;
    - `professor.current_card` returns `None` when card lists contains hidden
      cards only.
    """
    card_1 = copy.deepcopy(CARD_HIDDEN)
    card_2 = copy.deepcopy(CARD_BASIC_LEVEL2_1)
    card_3 = copy.deepcopy(CARD_HIDDEN)

    prof = doreen.ProfessorDoreen([card_1, card_2, card_3],
                                      date_mock=DateMock)
    
    current_card = prof.current_card
    assert current_card == card_2
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == None


def test_max_cards_per_grade():  # TODO: change rdates in CARD_BASIC_LEVEL0_X to be consistent with Doreen's policy with grade 0
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card` returns the expected cards ;
    - no more than `max_cards_per_grade` cards are reviewed ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_level0_age8 = copy.deepcopy(CARD_BASIC_LEVEL0_6)
    card_level0_age7 = copy.deepcopy(CARD_BASIC_LEVEL0_5)
    card_level0_age6 = copy.deepcopy(CARD_BASIC_LEVEL0_3)
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)
    card_level0_age3 = copy.deepcopy(CARD_BASIC_LEVEL0_4)

    card_list = [
            card_level0_age8,
            card_level0_age7,
            card_level0_age6,
            card_level0_age5,
            card_level0_age4,
            card_level0_age3,
        ]
    
    prof = doreen.ProfessorDoreen(card_list,
                                      date_mock=DateMock,
                                      max_cards_per_grade=3)

    current_card = prof.current_card
    assert current_card == card_level0_age8
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level0_age7
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level0_age6
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_level0_age5
    prof.current_card_reply(answer=WRONG_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level0_age3
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == None


def test_init_right_answer_current_grade():  # TODO: change rdates in CARD_BASIC_LEVEL0_X to be consistent with Doreen's policy with grade 0
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - right answers made today in a previous training session are counted in `self.num_right_answer_current_grade` (i.e. when the opencal executable has been called several time the same day) ;
    - `professor.current_card` returns the expected cards ;
    - no more than `max_cards_per_grade` cards are reviewed ;
    - `professor.current_card` returns `None` when there are no more cards to
      review.
    """
    card_reviewed_today_right_age6 = copy.deepcopy(CARD_REVIEWED_TODAY_2)   # formerly level 0
    card_reviewed_today_wrong_age5 = copy.deepcopy(CARD_REVIEWED_TODAY_3)
    card_reviewed_today_right_age1 = copy.deepcopy(CARD_REVIEWED_TODAY_1)   # formerly level -1

    card_level0_age8 = copy.deepcopy(CARD_BASIC_LEVEL0_6)
    card_level0_age7 = copy.deepcopy(CARD_BASIC_LEVEL0_5)
    card_level0_age6 = copy.deepcopy(CARD_BASIC_LEVEL0_3)
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)
    card_level0_age3 = copy.deepcopy(CARD_BASIC_LEVEL0_4)

    assert doreen.assess(card_reviewed_today_right_age6, date_mock=DateMock, ignore_today_answers=True) == 0
    assert doreen.assess(card_reviewed_today_right_age1, date_mock=DateMock, ignore_today_answers=True) == 0

    card_list = [
            card_reviewed_today_right_age6,
            card_reviewed_today_wrong_age5,
            card_reviewed_today_right_age1,
            card_level0_age8,
            card_level0_age7,
            card_level0_age6,
            card_level0_age5,
            card_level0_age4,
            card_level0_age3,
        ]

    prof = doreen.ProfessorDoreen(card_list,
                                      date_mock=DateMock,
                                      max_cards_per_grade=4)

    assert sorted(prof.num_right_answers_per_grade.keys()) == [0]
    assert prof.num_right_answers_per_grade[0] == 2

    current_card = prof.current_card
    assert current_card == card_level0_age8
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level0_age7
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_level0_age6
    prof.current_card_reply(answer=WRONG_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level0_age5
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == None


def test_switch_grade_min2():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor._switch_grade_loop` switch from level -2 to level 1 and from level -1 to level 1 ;
    """
    card_level_min2_age8 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_1)
    card_level_min2_age3 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_3)
    card_level_min2_age2 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_2)

    card_level_min1_age1 = copy.deepcopy(CARD_WITHOUT_REVIEW_1)
    card_level_min1_age2 = copy.deepcopy(CARD_WITHOUT_REVIEW_2)
    
    card_level0_age7 = copy.deepcopy(CARD_BASIC_LEVEL0_5)
    card_level0_age6 = copy.deepcopy(CARD_BASIC_LEVEL0_3)
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)
    card_level0_age3 = copy.deepcopy(CARD_BASIC_LEVEL0_4)
    
    card_level1_age10 = copy.deepcopy(CARD_BASIC_LEVEL1_1)

    card_list = [
            card_level_min2_age8,
            card_level_min2_age3,
            card_level_min2_age2,
            card_level_min1_age1,
            card_level_min1_age2,
            card_level0_age7,
            card_level0_age6,
            card_level0_age5,
            card_level0_age4,
            card_level0_age3,
            card_level1_age10,
        ]

    prof = doreen.ProfessorDoreen(card_list,
                                      date_mock=DateMock,
                                      max_cards_per_grade=2)

    current_card = prof.current_card
    assert current_card == card_level_min2_age8
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level_min2_age3
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == card_level1_age10
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == None


def test_switch_grade_min1():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor._switch_grade_loop` switch from level -2 to level 1 and from level -1 to level 1 ;
    """
    card_level_min2_age8 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_1)
    card_level_min2_age3 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_3)
    card_level_min2_age2 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_2)

    card_level_min1_age1 = copy.deepcopy(CARD_WITHOUT_REVIEW_1)
    card_level_min1_age2 = copy.deepcopy(CARD_WITHOUT_REVIEW_2)
    
    card_level0_age7 = copy.deepcopy(CARD_BASIC_LEVEL0_5)
    card_level0_age6 = copy.deepcopy(CARD_BASIC_LEVEL0_3)
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)
    card_level0_age3 = copy.deepcopy(CARD_BASIC_LEVEL0_4)
    
    card_level1_age10 = copy.deepcopy(CARD_BASIC_LEVEL1_1)

    card_list = [
            card_level_min2_age8,
            card_level_min2_age3,
            card_level_min2_age2,
            card_level_min1_age1,
            card_level_min1_age2,
            card_level0_age7,
            card_level0_age6,
            card_level0_age5,
            card_level0_age4,
            card_level0_age3,
            card_level1_age10,
        ]

    prof = doreen.ProfessorDoreen(card_list,
                                      date_mock=DateMock,
                                      max_cards_per_grade=2)

    current_card = prof.current_card
    assert current_card == card_level_min2_age8
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level_min2_age3
    prof.current_card_reply(answer=WRONG_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level_min2_age2
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_level_min1_age1
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == card_level1_age10
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == None


def test_several_cards():
    """Test `professor.current_card`, `professor._switch_grade_loop()` and `professor.current_card_reply()`.

    Check that:
    - `professor.current_card` returns the expected cards ;
    - no more than `max_cards_per_grade` cards are reviewed ;
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

    card_level_min2_age8 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_1)
    card_level_min2_age3 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_3)
    card_level_min2_age2 = copy.deepcopy(CARD_WRONG_REVIEW_YESTERDAY_2)

    card_level_min1_age1 = copy.deepcopy(CARD_WITHOUT_REVIEW_1)
    card_level_min1_age2 = copy.deepcopy(CARD_WITHOUT_REVIEW_2)
    
    card_level0_age7 = copy.deepcopy(CARD_BASIC_LEVEL0_5)
    card_level0_age6 = copy.deepcopy(CARD_BASIC_LEVEL0_3)
    card_level0_age5 = copy.deepcopy(CARD_BASIC_LEVEL0_2)
    card_level0_age4 = copy.deepcopy(CARD_BASIC_LEVEL0_1)
    card_level0_age3 = copy.deepcopy(CARD_BASIC_LEVEL0_4)
    
    card_level1_age10 = copy.deepcopy(CARD_BASIC_LEVEL1_1)

    card_level2_age17 = copy.deepcopy(CARD_BASIC_LEVEL2_3)
    card_level2_age12 = copy.deepcopy(CARD_IGNORE_FUTURE_REVIEWS)
    card_level2_age11 = copy.deepcopy(CARD_BASIC_LEVEL2_2)
    card_level2_age10 = copy.deepcopy(CARD_BASIC_LEVEL2_1)

    card_list = [
            card_hidden_age1,
            card_level_min3_age8,
            card_level_min3_age4,
            card_level_min3_age0,
            card_level_min2_age8,
            card_level_min2_age3,
            card_level_min2_age2,
            card_level_min1_age1,
            card_level_min1_age2,
            card_level0_age7,
            card_level0_age6,
            card_level0_age5,
            card_level0_age4,
            card_level0_age3,
            card_level1_age10,
            card_level2_age17,
            card_level2_age12,
            card_level2_age11,
            card_level2_age10,
        ]

    with pytest.warns(UserWarning):  # 'card_level2_age12' raises a UserWarning as it consains a rdate defined in the future
        prof = doreen.ProfessorDoreen(card_list,
                                    date_mock=DateMock,
                                    max_cards_per_grade=3)

    current_card = prof.current_card
    assert current_card == card_level_min2_age8
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level_min2_age3
    prof.current_card_reply(answer=WRONG_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level_min2_age2
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_level_min1_age1
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level_min1_age2
    prof.current_card_reply(answer=WRONG_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level0_age7
    prof.current_card_reply(answer="skip")

    current_card = prof.current_card
    assert current_card == card_level0_age6
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == card_level1_age10
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == card_level2_age17
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level2_age12
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    current_card = prof.current_card
    assert current_card == card_level2_age11
    prof.current_card_reply(answer=RIGHT_ANSWER_STR)

    ###

    current_card = prof.current_card
    assert current_card == None
