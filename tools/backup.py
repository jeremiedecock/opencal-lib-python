#!/usr/bin/env python3

# Src: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup

import opencal.io.sqlitedb

if __name__ == "__main__":
    opencal.io.sqlitedb.backup_db()