#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal
import opencal.path
import opencal.io.sqlitedb


if __name__ == "__main__":
    xml_file_path = opencal.path.expand_path(opencal.cfg["opencal"]["pkb_path"])
    sqlite_file_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])

    opencal.io.sqlitedb.xml_to_sqlite(
        xml_file_path=xml_file_path,
        sqlite_file_path=sqlite_file_path
    )
