#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal.path
import opencal.io.sqlitedb
import opencal.io.pkb
import os
import json
import sqlite3
import warnings

XML_FILE_NAME = "~/jeremie.pkb"


def fill_sqlite_tables():

    # Load the XML database ###################################################

    xml_file_path = opencal.path.expand_path(XML_FILE_NAME)
    card_list = opencal.io.pkb.load_pkb(xml_file_path)

    # Convert the XML data to SQL data ########################################

    sql_card_table_insert_params = []
    sql_review_table_insert_params = []

    last_review_id = 0

    for card_id, card_dict in enumerate(card_list):

        # Card ########################

        cdate = card_dict["cdate"]                   # TODO: convert to SQLite date format?
        hidden = card_dict["hidden"]
        question = card_dict["question"]      #.strip() # remove strip() because it generates fake differences with the original XML file
        answer = card_dict.get("answer", "")  #.strip()
        tag_list = card_dict["tags"]
        review_list = card_dict["reviews"]

        assert hidden in (True, False)
        hidden = int(hidden)

        tags_str = "\n".join(tag_list)

        sql_card_table_insert_params.append({
            "id": int(card_id),
            "creation_date": cdate,
            "hidden": hidden,
            "question": question,
            "answer": answer,
            "tags": tags_str
        })

        # Reviews #####################

        for review in review_list:

            review_id = last_review_id
            last_review_id += 1

            review_date = review["rdate"]               # TODO: convert to SQLite date format?
            result = review["result"]

            assert result in ('good','bad')

            sql_review_table_insert_params.append({
                "id": int(review_id),
                "card_id": card_id,
                "review_date": review_date,
                "result": result
            })

    # INSERT SQL DATA INTO THE CARD TABLE #######

    opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    sql_request = f"""INSERT INTO {opencal.io.sqlitedb.CARD_TABLE_NAME}
    ( id,  creation_date,  hidden,  question,  answer,  tags) VALUES
    (:id, :creation_date, :hidden, :question, :answer, :tags)
    """

    cur.executemany(sql_request, sql_card_table_insert_params)

    # INSERT SQL DATA INTO THE REVIEW TABLE #####

    sql_request = F"""INSERT INTO {opencal.io.sqlitedb.REVIEW_TABLE_NAME}
    ( id,  card_id,  review_date,  result) VALUES
    (:id, :card_id, :review_date, :result)
    """

    cur.executemany(sql_request, sql_review_table_insert_params)   # ERR: sqlite3.ProgrammingError: You did not supply a value for binding 2.

    con.commit()
    con.close()


#############################

if __name__ == "__main__":
    # opencal.io.sqlitedb.create_config_table()
    opencal.io.sqlitedb.create_card_table()
    opencal.io.sqlitedb.create_review_table()

    fill_sqlite_tables()