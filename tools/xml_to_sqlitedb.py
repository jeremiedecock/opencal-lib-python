#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal
import opencal.path
import opencal.io.sqlitedb
import opencal.io.pkb


if __name__ == "__main__":

    xml_file_path = opencal.path.expand_path(opencal.cfg["opencal"]["pkb_path"])
    sqlite_file_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])

    # Load the XML database ###################################################

    print("Loading from", xml_file_path)
    card_list = opencal.io.pkb.load_pkb(xml_file_path)

    # Save the database to SQLite ##############################################

    print("Saving to", sqlite_file_path)
    opencal.io.sqlitedb.save_pkb(
        card_list=card_list,
        opencal_db_path=sqlite_file_path
    )
