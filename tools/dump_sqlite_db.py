#!/usr/bin/env python3

# Convert SQLite DB file to SQL dump file dump.sql
# Src: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.iterdump

import opencal.io.sqlitedb

if __name__ == "__main__":
    opencal_db_path = opencal.cfg['opencal']['db_path']
    dump_file_path = opencal.cfg['opencal']['sqlite_dump_file_path']

    opencal.io.sqlitedb.dump_db(
        opencal_db_path=opencal_db_path,
        dump_file_path=dump_file_path
    )