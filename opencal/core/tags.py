import itertools
from typing import Any, Optional, Union, List, Dict

from opencal.card import Card

def tag_dict(
        card_list: List[Card],
        count_hidden_cards: bool = False
    ):
    tag_dict = {}

    for card in card_list:
        if not card.is_hidden or count_hidden_cards:
            for tag in card.tags:

                if tag not in tag_dict:
                    tag_dict[tag] = 0

                tag_dict[tag] += 1

    return tag_dict


def tag_list(
        card_list: List[Card],
        count_hidden_cards: bool = False,
        sort: str = "desc"
    ):
    reverse = True if sort == "desc" else False
    return sorted(tag_dict(card_list, count_hidden_cards).keys(), reverse=reverse)


def tag_list_count(
        card_list: List[Card],
        count_hidden_cards: bool = False,
        sort: str = "desc"
    ):
    reverse = True if sort == "desc" else False
    return sorted(tag_dict(card_list, count_hidden_cards).items(), key=lambda item: item[1], reverse=reverse)


def tag_edit(
        card_list: List[Card],
        from_tag: str,
        to_tag: str,
        edit_hidden_cards: bool = False
    ):
    for card in card_list:
        if not card.is_hidden or edit_hidden_cards:
            for index in range(len(card.tags)):
                if card.tags[index] == from_tag:
                    card.tags[index] = to_tag

    return card_list


def tag_graph(
        card_list: List[Card],
        count_hidden_cards: bool = False
    ):
    tag_dict = {}

    for card in card_list:
        if not card.is_hidden or count_hidden_cards:
            for pair in itertools.product(card.tags, repeat=2):

                if pair[0] != pair[1]:
                    if pair not in tag_dict:
                        tag_dict[pair] = 0

                    tag_dict[pair] += 1

    return {tuple(sorted(k)): v for k,v in tag_dict.items()}
