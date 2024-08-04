#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import opencal
import os
import sqlite3
from typing import Any, Dict, List, Optional

# from opencal.core.data import RIGHT_ANSWER_STR        # TODO: USE IT (OR REMOVE IT IN "pkb.py")!

PY_DATE_FORMAT = r"%Y-%m-%d"

# TIME_DELTA_OF_FIRST_REVIEWS = datetime.timedelta()    # Null time delta (0 day)    # TODO: USE IT (OR REMOVE IT IN "pkb.py")!
# INIT_VALIDATED_TIME_DELTA = datetime.timedelta()      # Null time delta (0 day)    # TODO: USE IT (OR REMOVE IT IN "pkb.py")!

CONFIG_TABLE_NAME = "t_config"
CARD_TABLE_NAME = "t_card"
ACQUISITION_REVIEW_TABLE_NAME = "t_acquisition_review"
CONSOLIDATION_REVIEW_TABLE_NAME = "t_consolidation_review"


# SAVE PKB ####################################################################

def save_pkb(
        card_list: List[Dict[str, Any]],
        opencal_db_path: os.PathLike
    ) -> None:
    """
    Save the personal knowledge base (PKB) to an SQLite database.

    This function takes a list of cards and saves them to the specified
    SQLite database. Each card contains information such as creation
    date, hidden status, question, answer, tags, and reviews.

    Note that this function is a temporary workaround until the database is fully integrated to the core of OpenCal.

    Parameters
    ----------
    card_list : List[Dict[str, Any]]
        A list of dictionaries where each dictionary represents a card with
        keys such as 'cdate', 'hidden', 'question', 'answer', 'tags', and 'reviews'.
    opencal_db_path : os.PathLike
        The SQLite database where the PKB should be saved.

    Returns
    -------
    None
    """

    opencal_db_path = opencal.path.expand_path(opencal_db_path)

    # Make sure the database exists otherwise create it
    if not os.path.exists(opencal_db_path):
        create_all_tables(opencal_db_path)

    # CONVERT THE CARD LIST TO SQL DATA #######################################

    sql_card_table_insert_params = []
    sql_review_table_insert_params = []

    last_review_id = 0

    for card_id, card_dict in enumerate(card_list):

        # Card ########################

        cdate = card_dict["cdate"]
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
            "creation_date": cdate.strftime(PY_DATE_FORMAT),
            "hidden": hidden,
            "question": question,
            "answer": answer,
            "tags": tags_str
        })

        # Reviews #####################

        for review in review_list:

            review_id = last_review_id
            last_review_id += 1

            review_date = review["rdate"]
            result = review["result"]

            assert result in ('good','bad')

            sql_review_table_insert_params.append({
                "id": int(review_id),
                "card_id": card_id,
                "review_date": review_date.strftime(PY_DATE_FORMAT),
                "result": result
            })

    # INSERT SQL DATA INTO THE CARD TABLE #####################################

    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    sql_request = f"""INSERT INTO {CARD_TABLE_NAME}
    ( id,  creation_date,  hidden,  question,  answer,  tags) VALUES
    (:id, :creation_date, :hidden, :question, :answer, :tags)
    """

    cur.executemany(sql_request, sql_card_table_insert_params)

    # INSERT SQL DATA INTO THE REVIEW TABLE #####

    sql_request = f"""INSERT INTO {CONSOLIDATION_REVIEW_TABLE_NAME}
    ( id,  card_id,  review_date,  result) VALUES
    (:id, :card_id, :review_date, :result)
    """

    cur.executemany(sql_request, sql_review_table_insert_params)

    con.commit()
    con.close()


# LOAD PKB ####################################################################

def load_pkb(opencal_db_path: os.PathLike) -> List[Dict[str, Any]]:
    """
    Load the personal knowledge base (PKB) from an SQLite database.

    This function reads the PKB from the specified SQLite database and parses
    it into a list of cards. Each card is represented as a dictionary with
    keys such as 'cdate', 'hidden', 'question', 'answer', 'tags', and 'reviews'.

    Note that this function is a temporary workaround until the database is fully integrated to the core of OpenCal.

    Parameters
    ----------
    opencal_db_path : os.PathLike
        The file path from which the PKB should be loaded.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries where each dictionary represents a card with
        keys such as 'cdate', 'hidden', 'question', 'answer', 'tags', and 'reviews'.
    """

    # opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])    # TODO: remove this line to the caller
    opencal_db_path = opencal.path.expand_path(opencal_db_path)

    # Make sure the database exists otherwise create it
    if not os.path.exists(opencal_db_path):
        create_all_tables(opencal_db_path)

    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # LOAD CARDS ######################

    cards_dict: Dict[int, Dict[str, Any]] = {}   # A dictionary containing all the cards

    sql_query_str = f"SELECT id, creation_date, hidden, question, answer, tags FROM {CARD_TABLE_NAME} ORDER BY id"

    # For each card in the database
    for row in cur.execute(sql_query_str):
        card_id: int
        card_creation_date_str: str
        is_hidden: int          # This boolean variable is stored as an integer as SQLite does not have a boolean type
        question: str
        answer: str
        tags_str: str

        card_id, card_creation_date_str, is_hidden, question, answer, tags_str = row

        card_creation_date = datetime.datetime.strptime(card_creation_date_str, PY_DATE_FORMAT) #.date()

        tags_str = tags_str.strip(" \t\r\n")        # Remove leading and trailing whitespaces, tabulations, and newlines
        tags_list = tags_str.split("\n")

        if tags_list == [""]:
            tags_list = []

        cards_dict[card_id] = {
            "cdate": card_creation_date,
            "hidden": bool(is_hidden),
            "question": question,
            "answer": answer,
            "reviews": [],        # List of dictionaries (each dictionary object is a *consolidation review* for this card)
            "tags": tags_list
        }

    # LOAD REVIEWS ####################

    sql_query_str = f"SELECT id, card_id, review_date, result FROM {CONSOLIDATION_REVIEW_TABLE_NAME} ORDER BY review_date"

    # For each *consolidation review* in the database
    for row in cur.execute(sql_query_str):
        review_id, card_id, review_date_str, result = row

        review_date = datetime.datetime.strptime(review_date_str, PY_DATE_FORMAT) #.date()

        review_dict = {
            "rdate": review_date,
            "result": result
        }

        cards_dict[card_id]["reviews"].append(review_dict)

    con.close()

    # Sort the dictionary items **by key** and then extracts the values, resulting in a list of cards **sorted by their IDs**.
    cards_list = [card for _, card in sorted(cards_dict.items())]

    # Sort reviews for each card by date
    for card_dict in cards_list:
        card_dict["reviews"] = sorted(card_dict["reviews"], key=lambda review_dict: review_dict["rdate"])

    return cards_list


###############################################################################


def create_all_tables(opencal_db_path: os.PathLike) -> None:
    """
    Create all necessary tables in the SQLite database.

    This function creates the configuration, card, acquisition and
    consolidation review tables in the SQLite database located at the specified
    path.

    Parameters
    ----------
    opencal_db_path : os.PathLike
        The path to the SQLite database file.

    Returns
    -------
    None
    """
    create_config_table(opencal_db_path)
    create_card_table(opencal_db_path)
    create_consolidation_review_table(opencal_db_path)
    create_acquisition_review_table(opencal_db_path)


def create_config_table(opencal_db_path: os.PathLike) -> None:
    print(f"Initializing table {CONFIG_TABLE_NAME} in database {opencal_db_path}")

    opencal_db_path = opencal.path.expand_path(opencal_db_path)

    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # DELETE TABLE ##############

    print(f"Deleting table {CONFIG_TABLE_NAME} before re-creating it...")

    try:
        cur.execute(f"DROP TABLE {CONFIG_TABLE_NAME}")
    except sqlite3.OperationalError as e:
        # The database does not exist
        print(e)

    # CREATE TABLE ##############

    print(f"Creating table {CONFIG_TABLE_NAME}...")

    sql_query_str = f"""CREATE TABLE {CONFIG_TABLE_NAME} (
        key            TEXT PRIMARY KEY,
        value          TEXT
    )"""

    cur.execute(sql_query_str)
    con.commit()
    con.close()


def create_card_table(opencal_db_path: os.PathLike) -> None:
    print(f"Initializing table {CARD_TABLE_NAME} in database {opencal_db_path}")

    opencal_db_path = opencal.path.expand_path(opencal_db_path)

    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # DELETE TABLE ##############

    print(f"Deleting table {CARD_TABLE_NAME} before re-creating it...")

    try:
        cur.execute(f"DROP TABLE {CARD_TABLE_NAME}")
    except sqlite3.OperationalError as e:
        # The database does not exist
        print(e)

    # CREATE TABLE ##############

    print(f"Creating table {CARD_TABLE_NAME}...")

    sql_query_str = f"""CREATE TABLE {CARD_TABLE_NAME} (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        creation_date   TEXT DEFAULT CURRENT_TIMESTAMP,
        hidden          INTEGER DEFAULT 0,
        question        TEXT NOT NULL,
        answer          TEXT,
        tags            TEXT NOT NULL
    )"""

    cur.execute(sql_query_str)
    con.commit()
    con.close()


def create_consolidation_review_table(opencal_db_path: os.PathLike) -> None:
    print(f"Initializing table {CONSOLIDATION_REVIEW_TABLE_NAME} in database {opencal_db_path}")

    opencal_db_path = opencal.path.expand_path(opencal_db_path)

    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # DELETE TABLE ##############

    print(f"Deleting table {CONSOLIDATION_REVIEW_TABLE_NAME} before re-creating it...")

    try:
        cur.execute(f"DROP TABLE {CONSOLIDATION_REVIEW_TABLE_NAME}")
    except sqlite3.OperationalError as e:
        # The database does not exist
        print(e)

    # CREATE TABLE ##############

    print(f"Creating table {CONSOLIDATION_REVIEW_TABLE_NAME}...")

    sql_query_str = f"""CREATE TABLE {CONSOLIDATION_REVIEW_TABLE_NAME} (
        id                   INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id              INTEGER NOT NULL,
        review_date          TEXT DEFAULT CURRENT_TIMESTAMP,
        result               TEXT CHECK( result IN ('good','bad') ) NOT NULL,
        FOREIGN KEY(card_id) REFERENCES {CARD_TABLE_NAME}(id)
    )"""

    cur.execute(sql_query_str)
    con.commit()
    con.close()


def create_acquisition_review_table(opencal_db_path: os.PathLike) -> None:
    print(f"Initializing table {ACQUISITION_REVIEW_TABLE_NAME} in database {opencal_db_path}")

    opencal_db_path = opencal.path.expand_path(opencal_db_path)

    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # DELETE TABLE ##############

    print(f"Deleting table {ACQUISITION_REVIEW_TABLE_NAME} before re-creating it...")

    try:
        cur.execute(f"DROP TABLE {ACQUISITION_REVIEW_TABLE_NAME}")
    except sqlite3.OperationalError as e:
        # The database does not exist
        print(e)

    # CREATE TABLE ##############

    print(f"Creating table {ACQUISITION_REVIEW_TABLE_NAME}...")

    sql_query_str = f"""CREATE TABLE {ACQUISITION_REVIEW_TABLE_NAME} (
        id                   INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id              INTEGER NOT NULL,
        review_datetime      TEXT DEFAULT CURRENT_TIMESTAMP,
        review_duration_ms   INTEGER NOT NULL,
        is_right_answer      INTEGER NOT NULL,
        FOREIGN KEY(card_id) REFERENCES {CARD_TABLE_NAME}(id)
    )"""

    cur.execute(sql_query_str)
    con.commit()
    con.close()


def backup_db(
        opencal_db_path: os.PathLike,
        backup_dir_path: os.PathLike,
        prefix: str = ""
    ) -> None:
    """
    Create a backup of the SQLite database.

    This function creates a backup of the SQLite database located at the specified
    path and saves it to the specified backup directory with an optional prefix
    and the current date appended to the filename.

    Parameters
    ----------
    opencal_db_path : os.PathLike
        The path to the SQLite database file to be backed up.
    backup_dir_path : os.PathLike
        The path to the directory where the backup file will be saved.
    prefix : str, optional
        An optional prefix to add to the backup file name (default is "").

    Returns
    -------
    None
    """
    today_str = datetime.datetime.now().strftime(r"%Y-%m-%d")

    opencal_db_path = opencal.path.expand_path(opencal_db_path)
    backup_file_path = os.path.join(opencal.path.expand_path(backup_dir_path), prefix + today_str + "_opencal.sqlite")

    def progress(status, remaining, total):
        # print(f'Copied {total-remaining} of {total} pages...')
        print(".", end="")

    src_db = sqlite3.connect(opencal_db_path)
    dst_db = sqlite3.connect(backup_file_path)

    with dst_db:
        src_db.backup(dst_db, pages=1, progress=progress)

    dst_db.close()
    src_db.close()

    print("Database cloned in", backup_file_path)


def dump_db(
        opencal_db_path: os.PathLike,
        dump_dir_path: os.PathLike
    ) -> None:
    """
    Dump the SQLite database to a SQL file.

    This function creates a SQL dump of the SQLite database located at the specified
    path and saves it to the specified dump directory.

    Parameters
    ----------
    opencal_db_path : os.PathLike
        The path to the SQLite database file to be dumped.
    dump_dir_path : os.PathLike
        The path to the directory where the dump file will be saved.

    Returns
    -------
    None
    """
    opencal_db_path = opencal.path.expand_path(opencal_db_path)
    dump_file_path = os.path.join(opencal.path.expand_path(dump_dir_path), "opencal.sql")

    con = sqlite3.connect(opencal_db_path)

    with open(dump_file_path, 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)

    con.close()

    print("Database dumped in", dump_file_path)


def restore_db(
        opencal_db_path: os.PathLike,
        dump_dir_path: os.PathLike
    ) -> None:
    """
    Restore the SQLite database from a SQL dump file.

    This function restores the SQLite database located at the specified path
    from a SQL dump file located in the specified dump directory. If the
    original database exists, it creates a backup before restoring.

    Parameters
    ----------
    opencal_db_path : os.PathLike
        The path to the SQLite database file to be restored.
    dump_dir_path : os.PathLike
        The path to the directory where the dump file is located.

    Returns
    -------
    None
    """
    opencal_db_path = opencal.path.expand_path(opencal_db_path)
    dump_file_path = os.path.join(opencal.path.expand_path(dump_dir_path), "opencal.sql")

    # Backup the original database if it exists
    if os.path.exists(opencal_db_path):
        backup_db(prefix="before_restore_")
        print("Backup created")

    con = sqlite3.connect(opencal_db_path)

    # Delete all tables in the database
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # tables = [
    #     "t_config",
    #     "t_card",
    #     "t_acquisition_review",
    #     "t_consolidation_review"
    # ]

    for table_name in tables:
        if table_name[0] != "sqlite_sequence":
            cursor.execute(f'DROP TABLE IF EXISTS {table_name[0]};')
    con.commit()

    # Restore the database from the dump file
    with open(dump_file_path, 'r') as fd:
        sql = fd.read()
        con.executescript(sql)

    con.close()

    print("Database restored from", dump_file_path)


# DEBUG #######################################################################

def main() -> None:
    """
    Main function to load and save the personal knowledge base (PKB).

    This function loads the PKB from the path specified in the configuration
    then save it in another file.

    This function is used for debugging purposes (c.f. `.vscode/launch.json`).

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    load_pkb_path = opencal.cfg['opencal']['db_path']
    save_pkb_path = "/tmp/debug.sqlite"   # opencal.cfg["opencal"]["db_path"]

    print(f"Loading PKB from {load_pkb_path}")
    card_list = load_pkb(load_pkb_path)

    # print(card_list)

    print(f"Saving PKB to {save_pkb_path}")
    save_pkb(card_list, save_pkb_path)


if __name__ == "__main__":
    main()
