import pandas as pd
import copy
from opencal.card import Card
from typing import List, Tuple

RIGHT_ANSWER_STR = "good"
WRONG_ANSWER_STR = "bad"

def card_list_to_dataframes(
        card_list: List[Card]
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    flat_card_list = []
    flat_review_list = []

    card_id = 0

    for card in card_list:
        card = copy.deepcopy(card)

        del card["question"]
        del card["answer"]
        del card["tags"]

        review_list = card.consolidation_reviews

        for review in review_list:
            review["card_id"] = card_id

        flat_review_list.extend(review_list)

        del card["reviews"]

        flat_card_list.append(card)

        card_id += 1

    card_df = pd.DataFrame(flat_card_list)
    review_df = pd.DataFrame(flat_review_list)

    return card_df, review_df