#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal

import datetime
import os
import sqlite3

CONFIG_TABLE_NAME = "t_config"
CARD_TABLE_NAME = "t_card"
REVIEW_TABLE_NAME = "t_review"


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