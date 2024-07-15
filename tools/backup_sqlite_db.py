#!/usr/bin/env python3

# Src: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup

import opencal.io.sqlitedb

if __name__ == "__main__":
    opencal_db_path = opencal.cfg['opencal']['db_path']
    backup_dir_path = opencal.cfg['opencal']['db_backup_path']

    opencal.io.sqlitedb.backup_db(
        opencal_db_path=opencal_db_path,
        backup_dir_path=backup_dir_path
    )
