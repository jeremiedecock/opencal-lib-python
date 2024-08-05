import datetime
from opencal.core.professor.professor import AbstractProfessor
from opencal.io.sqlitedb import ACQUISITION_REVIEW_TABLE_NAME, CARD_TABLE_NAME, PY_DATE_FORMAT

class AbstractAcquisitionProfessor(AbstractProfessor):

    def save_current_card_reply(
        self,
        card: dict,
        review_duration_ms: int,
        is_right_answer: bool
    ) -> None:
        """
        Save the current card reply in the database.

        This function saves the reply for the current card being reviewed into
        the database. It records the card ID, the review date and time, the 
        duration of the review, and whether the answer was correct.

        Parameters
        ----------
        card : dict
            The card being reviewed.
        review_duration_ms : int
            The duration of the review in milliseconds.
        is_right_answer : bool
            A boolean indicating whether the answer was correct.

        Returns
        -------
        None
        """

        import warnings

        # Retrieve the card ID ##################

        hidden = card["hidden"]
        assert hidden in (True, False)
        hidden = int(hidden)

        tag_list = card["tags"]
        tags_str = "\n".join(tag_list)

        sql_query = f"SELECT id FROM {CARD_TABLE_NAME} WHERE creation_date=? AND question=? AND answer=? AND hidden=? AND tags=?"
        self.cur.execute(sql_query, (card['cdate'].strftime(PY_DATE_FORMAT), card['question'], card['answer'], hidden, tags_str))
        rows = self.cur.fetchall()

        if rows:
            card_id = rows[0][0]
            if len(rows) > 1:
                warnings.warn("More than one record found for the (creation_date, question, answer, hidden, tags) tuple.")
        else:
            raise ValueError("No card ID found in the database.")

        # Save the reply in the database ########

        current_datetime = datetime.datetime.now().astimezone(tz=None)  # Get the current date and time in the local timezone
        current_datetime_str = datetime.datetime.isoformat(current_datetime)

        sql_request_values_dict = {
            "card_id": card_id,
            "review_datetime": current_datetime_str,
            "review_duration_ms": review_duration_ms,
            "is_right_answer": is_right_answer
        }

        sql_request = f"""INSERT INTO {ACQUISITION_REVIEW_TABLE_NAME}
        ( card_id,  review_datetime,  review_duration_ms,  is_right_answer) VALUES
        (:card_id, :review_datetime, :review_duration_ms, :is_right_answer)
        """

        # This is the qmark style:
        self.cur.execute(sql_request, sql_request_values_dict)
        self.con.commit()
