#!/usr/bin/env python3

# Convert SQLite DB file to SQL dump file dump.sql
# Src: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.iterdump

import opencal.io.sqlitedb

opencal.io.sqlitedb.dump_db()