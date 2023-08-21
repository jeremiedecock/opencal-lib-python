#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal.path
import opencal.io.sqlitedb
import opencal.io.pkb

XML_FILE_PATH = "~/opencal_pkb.xml"

if __name__ == "__main__":
    card_list = opencal.io.sqlitedb.load_db()

    print("writing to", XML_FILE_PATH)
    opencal.io.pkb.save_pkb(card_list, opencal.path.expand_path(XML_FILE_PATH))
