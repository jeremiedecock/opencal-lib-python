#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal
import opencal.path
import opencal.io.sqlitedb
import opencal.io.pkb


if __name__ == "__main__":

    xml_file_path_src = opencal.path.expand_path(opencal.cfg["opencal"]["pkb_path"])
    sqlite_file_path =  "/tmp/pkb.sqlite"      # opencal.path.expand_path(opencal.cfg['opencal']['db_path'])
    xml_file_path_dst = "/tmp/pkb.xml"         # opencal.path.expand_path(opencal.cfg["opencal"]["pkb_path"])

    # Load the XML database ###################################################

    print("Loading from", xml_file_path_src)
    card_list = opencal.io.pkb.load_pkb(xml_file_path_src)

    # Save the database to SQLite ##############################################

    print("Saving to", sqlite_file_path)
    opencal.io.sqlitedb.save_pkb(
        card_list=card_list,
        opencal_db_path=sqlite_file_path
    )

    # Load the SQLite database ################################################

    print("Loading from", sqlite_file_path)
    card_list = opencal.io.sqlitedb.load_pkb(sqlite_file_path)

    # Save the database to XML file ###########################################

    print("Saving to", xml_file_path_dst)
    opencal.io.pkb.save_pkb(
        card_list=card_list,
        pkb_path=xml_file_path_dst
    )
