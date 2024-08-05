import datetime
from opencal.core.professor.professor import AbstractProfessor
from opencal.io.sqlitedb import ACQUISITION_REVIEW_TABLE_NAME, CARD_TABLE_NAME, PY_DATE_FORMAT
from typing import Optional

class AbstractAcquisitionProfessor(AbstractProfessor):

    def update_card_list(
            self,
            card_list: list,
            review_hidden_cards: bool = False
        ):
        raise NotImplementedError()


    def save_current_card_reply(
        self,
        card: dict,
        is_right_answer: bool,
        user_response_time_ms: Optional[int] = None
    ) -> None:
        """
        Save the current card reply in the database.

        This function saves the reply for the current card being reviewed into
        the database. It records the card ID, the review date and time, the 
        user's response time (in milliseconds), and whether the answer was correct.

        Parameters
        ----------
        card : dict
            The card being reviewed.
        is_right_answer : bool
            A boolean indicating whether the answer was correct.
        user_response_time_ms : Optional[int], optional
            The time taken by the user to respond, in milliseconds (default is None).

        Returns
        -------
        None
        """

        import warnings

        # Retrieve the card ID ##################

        is_hidden = card["hidden"]
        assert is_hidden in (True, False)
        is_hidden = int(is_hidden)

        tag_list = card["tags"]
        tags_str = "\n".join(tag_list)

        sql_query = f"SELECT id FROM {CARD_TABLE_NAME} WHERE creation_datetime=? AND question=? AND answer=? AND is_hidden=? AND tags=?"
        self.cur.execute(sql_query, (card['cdate'].strftime(PY_DATE_FORMAT), card['question'], card['answer'], is_hidden, tags_str))
        rows = self.cur.fetchall()

        if rows:
            card_id = rows[0][0]
            if len(rows) > 1:
                warnings.warn("More than one record found for the (creation_datetime, question, answer, is_hidden, tags) tuple.")
        else:
            raise ValueError("No card ID found in the database.")

        # Save the reply in the database ########

        current_datetime = datetime.datetime.now().astimezone(tz=None)  # Get the current date and time in the local timezone
        current_datetime_str = datetime.datetime.isoformat(current_datetime)

        sql_request_values_dict = {
            "card_id": card_id,
            "review_datetime": current_datetime_str,
            "user_response_time_ms": user_response_time_ms,
            "is_right_answer": is_right_answer
        }

        sql_request = f"""INSERT INTO {ACQUISITION_REVIEW_TABLE_NAME}
        ( card_id,  review_datetime,  user_response_time_ms,  is_right_answer) VALUES
        (:card_id, :review_datetime, :user_response_time_ms, :is_right_answer)
        """

        # This is the qmark style:
        self.cur.execute(sql_request, sql_request_values_dict)
        self.con.commit()
