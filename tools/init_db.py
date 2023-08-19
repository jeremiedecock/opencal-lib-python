#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal.io.database


#############################

if __name__ == "__main__":
    # opencal.io.database.create_config_table()
    opencal.io.database.create_card_table()
    opencal.io.database.create_review_table()

    # fill_task_table()
    # fill_micro_task_planning_table()