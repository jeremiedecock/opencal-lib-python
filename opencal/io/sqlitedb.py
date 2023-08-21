#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal

import datetime
import os
import sqlite3

CONFIG_TABLE_NAME = "t_config"
CARD_TABLE_NAME = "t_card"
REVIEW_TABLE_NAME = "t_review"


# LOAD PKB ####################################################################

def load_db():

    opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # LOAD CARDS ######################

    data_dict = {}

    sql_query_str = f"SELECT id, creation_date, hidden, question, answer, tags FROM {CARD_TABLE_NAME} ORDER BY id"

    for row in cur.execute(sql_query_str):
        _id, creation_date_str, hidden, question, answer, tag_str = row

        creation_date = datetime.datetime.strptime(creation_date_str, r"%Y-%m-%d %H:%M:%S")
        tag_list = tag_str.split("\n")

        if tag_list == [""]:
            tag_list = []

        data_dict[_id] = {
            "cdate": creation_date,
            "hidden": bool(hidden),
            "question": question,
            "answer": answer,
            "reviews": [],
            "tags": tag_list
        }

    # LOAD REVIEWS ####################

    sql_query_str = f"SELECT id, card_id, review_date, result FROM {REVIEW_TABLE_NAME} ORDER BY review_date"

    for row in cur.execute(sql_query_str):
        _id, card_id, review_date_str, result = row

        review_date = datetime.datetime.strptime(review_date_str, r"%Y-%m-%d %H:%M:%S")

        review_dict = {
            "rdate": review_date,
            "result": result
        }

        data_dict[card_id]["reviews"].append(review_dict)

    con.close()

    # Write in `card_list` the `data_dict` values sorted by `data_dict` keys
    card_list = [data_dict[_id] for _id in sorted(data_dict.keys())]

    return card_list


###############################################################################

# def create_config_table():
#     opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
#     con = sqlite3.connect(opencal_db_path)
#     cur = con.cursor()
#
#     # DELETE TABLE ##############
#
#     try:
#         cur.execute(f"DROP TABLE {CONFIG_TABLE_NAME}")
#     except sqlite3.OperationalError as e:
#         # The database does not exist
#         print(e)
#
#     # CREATE TABLE ##############
#
#     sql_query_str = f"""CREATE TABLE {CONFIG_TABLE_NAME} (
#         key            TEXT PRIMARY KEY,
#         value          TEXT
#     )"""
#
#     cur.execute(sql_query_str)
#     con.commit()
#     con.close()


def create_card_table():
    print(f"Initializing table {CARD_TABLE_NAME} in database {opencal.cfg['opencal']['db_path']}")

    opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # DELETE TABLE ##############

    try:
        cur.execute(f"DROP TABLE {CARD_TABLE_NAME}")
    except sqlite3.OperationalError as e:
        # The database does not exist
        print(e)

    # CREATE TABLE ##############

    sql_query_str = f"""
CREATE TABLE {CARD_TABLE_NAME} (
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


def create_review_table():
    print(f"Initializing table {REVIEW_TABLE_NAME} in database {opencal.cfg['opencal']['db_path']}")

    opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    con = sqlite3.connect(opencal_db_path)
    cur = con.cursor()

    # DELETE TABLE ##############

    try:
        cur.execute(f"DROP TABLE {REVIEW_TABLE_NAME}")
    except sqlite3.OperationalError as e:
        # The database does not exist
        print(e)

    # CREATE TABLE ##############

    sql_query_str = f"""
CREATE TABLE {REVIEW_TABLE_NAME} (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id              INTEGER NOT NULL,
    review_date          TEXT DEFAULT CURRENT_TIMESTAMP,
    result               TEXT CHECK( result IN ('good','bad') ) NOT NULL,
    FOREIGN KEY(card_id) REFERENCES {CARD_TABLE_NAME}(id)
)"""

    cur.execute(sql_query_str)
    con.commit()
    con.close()


def backup_db():
    today_str = datetime.datetime.now().strftime(r"%Y-%m-%d")

    opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    backup_file_path = os.path.join(opencal.path.expand_path(opencal.cfg['opencal']['db_backup_path']), today_str + "_opencal.sqlite")

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


def dump_db():
    opencal_db_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    dump_file_path = os.path.join(opencal.path.expand_path(opencal.cfg['opencal']['db_backup_path']), "opencal.sql")

    con = sqlite3.connect(opencal_db_path)

    with open(dump_file_path, 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)

    con.close()

    print("Database dumped in", dump_file_path)