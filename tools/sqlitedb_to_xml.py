#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal.path
import opencal.io.sqlitedb
import opencal.io.pkb

if __name__ == "__main__":

    sqlite_file_path = opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    xml_file_path = opencal.path.expand_path(opencal.cfg["opencal"]["pkb_path"])

    # Load the SQLite database ################################################

    print("Loading from", sqlite_file_path)
    card_list = opencal.io.sqlitedb.load_pkb(sqlite_file_path)

    # Save the database to XML file ###########################################

    print("Saving to", xml_file_path)
    opencal.io.pkb.save_pkb(
        card_list=card_list,
        pkb_path=xml_file_path
    )
