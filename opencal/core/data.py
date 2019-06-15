import pandas as pd
import copy

RIGHT_ANSWER_STR = "good"
WRONG_ANSWER_STR = "bad"

def card_list_to_dataframes(card_list):
    flat_card_list = []
    flat_review_list = []

    card_id = 0

    for card in card_list:
        card = copy.deepcopy(card)

        del card["question"]
        del card["answer"]
        del card["tags"]

        if "reviews" in card.keys():
            review_list = card["reviews"]

            for review in review_list:
                review["card_id"] = card_id

            flat_review_list.extend(review_list)

            del card["reviews"]

        flat_card_list.append(card)

        card_id += 1

    card_df = pd.DataFrame(flat_card_list)
    review_df = pd.DataFrame(flat_review_list)

    return card_df, review_df