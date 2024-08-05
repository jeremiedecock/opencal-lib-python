#!/usr/bin/env python3

# Restore the SQLite database from a SQL dump file

import opencal.io.sqlitedb

if __name__ == "__main__":
    opencal_db_path = opencal.cfg['opencal']['db_path']
    dump_file_path = opencal.cfg['opencal']['sqlite_dump_file_path']
    backup_dir_path = opencal.cfg['opencal']['sqlite_backup_dir_path']

    opencal.io.sqlitedb.restore_db(
        opencal_db_path=opencal_db_path,
        dump_file_path=dump_file_path,
        backup_dir_path=backup_dir_path
    )
