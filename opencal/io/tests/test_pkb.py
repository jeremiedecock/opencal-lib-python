#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.io.pkb" module.
"""

import opencal.io.pkb

import datetime
import numpy as np
import os
import pytest
import tempfile

# Test the "load_pkb" and "save_pkb" functions ################################

PKB_1_BASIC_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[Première question.]]></question>
<answer><![CDATA[Première réponse.]]></answer>
<tag>tag 1</tag>
</card>
<card cdate="2008-04-02" hidden="true">
<question><![CDATA[Deuxième question.]]></question>
<answer><![CDATA[Deuxième réponse.]]></answer>
<tag>tag 1</tag>
<tag>tag 2</tag>
<review rdate="2008-04-16" result="bad"/>
<review rdate="2008-05-23" result="good"/>
</card>
</pkb>
"""

PKB_2_MULTILINES_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[Première...
question.]]></question>
<answer><![CDATA[Première...
réponse.]]></answer>
<tag>tag 1</tag>
</card>
<card cdate="2008-04-02" hidden="true">
<question><![CDATA[Deuxième...
question.]]></question>
<answer><![CDATA[Deuxième...
réponse.]]></answer>
<tag>tag 1</tag>
<tag>tag 2</tag>
<review rdate="2008-04-16" result="bad"/>
<review rdate="2008-05-23" result="good"/>
</card>
</pkb>
"""

PKB_3_UTF8_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2011-06-10" hidden="true">
<question><![CDATA[Comment dit-on "Je / moi" en japonais (ie comment l'écrit-on en romaji) ?
Comment l'écrit-on en hiragana ?]]></question>
<answer><![CDATA[romaji   : watashi
hiragana : わたし

"watashi" semble être écrit plus couramment en kanji (qu'en hiragana).]]></answer>
<tag>japonais</tag>
<review rdate="2011-06-11" result="bad"/>
<review rdate="2011-06-12" result="bad"/>
<review rdate="2011-06-13" result="bad"/>
<review rdate="2011-06-14" result="bad"/>
</card>
<card cdate="2011-06-16" hidden="true">
<question><![CDATA[Comment écrit-on "bonjour !" en pinyin ?
Comment le prononce-t-on ?]]></question>
<answer><![CDATA[nǐ hǎo ! (你好 !) à prononcer "nii hao"


MÉMO :
- nǐ  (你) = tu, toi
- hǎo (好) = bon, bien]]></answer>
<tag>chinois</tag>
<tag>pinyin</tag>
<tag>prononciation</tag>
<review rdate="2011-06-17" result="good"/>
<review rdate="2011-06-19" result="good"/>
<review rdate="2011-06-23" result="good"/>
<review rdate="2011-07-01" result="good"/>
<review rdate="2011-07-17" result="good"/>
<review rdate="2011-08-18" result="good"/>
<review rdate="2011-10-21" result="good"/>
<review rdate="2012-03-03" result="good"/>
</card>
</pkb>
"""

PKB_4_XML_TAGS_EMBEDDED_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[Cette question contient <b>une balise XML</b>.]]></question>
<answer><![CDATA[Cette question contient une fause <balise>.]]></answer>
<tag>tag 1</tag>
</card>
<card cdate="2008-04-02" hidden="true">
<question><![CDATA[Cette question contient </question></card><card><question>une tentative d'injection de code XML.]]></question>
<answer><![CDATA[Et cette réponse </answer><answer>aussi.]]></answer>
<tag>tag 1</tag>
<tag>tag 2</tag>
<review rdate="2008-04-16" result="bad"/>
<review rdate="2008-05-23" result="good"/>
</card>
</pkb>
"""

PKB_5_EMPTY_ANSWER_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[Question.]]></question>
<answer/>
<tag>tag 1</tag>
</card>
</pkb>
"""

PKB_6_EMPTY_CARD_LIST_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
</pkb>
"""

PKB_7_CDATA_NESTING_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[foo]]]]><![CDATA[>bar]]]]><![CDATA[>baz]]></question>
<answer/>
<tag>tag 1</tag>
</card>
</pkb>
"""

PKB_8_SOME_SPECIAL_CHARS_STR = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[{} \" \\\" > # // % $ &]]></question>
<answer/>
<tag>tag 1</tag>
</card>
</pkb>
"""

PKB_9_REVIEWS_NOT_SORTED_PROVIDED_INPUT = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[Foo]]></question>
<answer/>
<tag>tag 1</tag>
<review rdate="2008-01-10" result="bad"/>
<review rdate="2008-01-15" result="good"/>
<review rdate="2008-01-11" result="bad"/>
<review rdate="2008-01-07" result="good"/>
</card>
</pkb>
"""

PKB_9_REVIEWS_NOT_SORTED_EXPECTED_OUTPUT = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pkb>
<card cdate="2008-04-02" hidden="false">
<question><![CDATA[Foo]]></question>
<answer/>
<tag>tag 1</tag>
<review rdate="2008-01-07" result="good"/>
<review rdate="2008-01-10" result="bad"/>
<review rdate="2008-01-11" result="bad"/>
<review rdate="2008-01-15" result="good"/>
</card>
</pkb>
"""

def load_save_and_compare(pkb_str, expected_output=None):
    """Check whether successives load and save keep the original file identical."""

    # Create a temporary file and parse it ######

    with tempfile.NamedTemporaryFile(mode='w') as tf:
        tf.write(pkb_str)
        tf.file.flush()

        pkb_path = tf.name

        card_list = opencal.io.pkb.load_pkb(pkb_path)
    
    # Here the temp file is closed and removed

    # Save ######################################

    opencal.io.pkb.save_pkb(card_list, pkb_path)

    # Read and saved file #######################

    with open(pkb_path) as df:
        saved_str = df.read()

    os.remove(pkb_path)

    # Test ######################################

    if expected_output is not None:
        assert saved_str == expected_output
    else:
        assert saved_str == pkb_str


def test_load_pkb_and_save_pkb_basic():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_1_BASIC_STR)

def test_load_pkb_and_save_pkb_multilines():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_2_MULTILINES_STR)

def test_load_pkb_and_save_pkb_utf8():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_3_UTF8_STR)

def test_load_pkb_and_save_pkb_xml_embedded():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_4_XML_TAGS_EMBEDDED_STR)

def test_load_pkb_and_save_pkb_empty_answer():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_5_EMPTY_ANSWER_STR)

def test_load_pkb_and_save_pkb_empty_card_list():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_6_EMPTY_CARD_LIST_STR)

def test_load_pkb_and_save_pkb_cdata_nesting():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_7_CDATA_NESTING_STR)

def test_load_pkb_and_save_pkb_special_chars():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_8_SOME_SPECIAL_CHARS_STR)

def test_load_pkb_and_save_pkb_reviews_not_sorted():
    """Check whether successives load and save keep the original file identical."""
    load_save_and_compare(PKB_9_REVIEWS_NOT_SORTED_PROVIDED_INPUT, PKB_9_REVIEWS_NOT_SORTED_EXPECTED_OUTPUT)


def test_load_pkb_err_empty_cdate():
    pkb_str = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <pkb>
    <card cdate="" hidden="false">
    <question><![CDATA[Question.]]></question>
    <answer/>
    <tag>tag 1</tag>
    </card>
    </pkb>
    """

    with tempfile.NamedTemporaryFile(mode='w') as tf:
        tf.write(pkb_str)
        tf.file.flush()

        pkb_path = tf.name

        #with pytest.raises(opencal.io.pkb.XmlPkbError):   # TODO ?
        with pytest.raises(ValueError):
            card_list = opencal.io.pkb.load_pkb(pkb_path)


def test_save_pkb_cdata_nesting():
    card_list = [{'reviews': [],
                  'tags': ['tag 1'],
                  'cdate': datetime.datetime(2018, 1, 1, 0, 0),
                  'hidden': False,
                  'question': 'This is ]]></question><answer/><tag>Hack</tag></card><card cdate="2018-01-02" hidden="false"><question><![CDATA[an XML code injection example',
                  'answer': ''}]

    with tempfile.NamedTemporaryFile(mode='w') as tf:
        pkb_path = tf.name

    # Here the temp file is closed and removed

    # Save ######################################

    opencal.io.pkb.save_pkb(card_list, pkb_path)

    # Read saved file ###########################

    saved_card_list = opencal.io.pkb.load_pkb(pkb_path)

    os.remove(pkb_path)

    # Test ######################################

    assert len(card_list) == len(saved_card_list)     # If the XML code injection succedded then we have two cards instead of one
    assert card_list[0]['question'] == saved_card_list[0]['question']  # Question is modified if the XML code injection succedded


def test_save_pkb_cdata_nesting_2():
    card_list = [{'reviews': [],
                  'tags': ['tag 1'],
                  'cdate': datetime.datetime(2018, 1, 1, 0, 0),
                  'hidden': False,
                  'question': 'foo]]>bar]]>baz',
                  'answer': ''}]

    with tempfile.NamedTemporaryFile(mode='w') as tf:
        pkb_path = tf.name

    # Here the temp file is closed and removed

    # Save ######################################

    opencal.io.pkb.save_pkb(card_list, pkb_path)

    # Read saved file ###########################

    saved_card_list = opencal.io.pkb.load_pkb(pkb_path)

    os.remove(pkb_path)

    # Test ######################################

    assert len(card_list) == len(saved_card_list)     # If the XML code injection succedded then we have two cards instead of one
    assert card_list[0]['question'] == saved_card_list[0]['question']  # Question is modified if the XML code injection succedded
