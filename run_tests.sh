#!/bin/bash

PYTHON="/usr/bin/env python3"

#./setup_db.sh

TEST_DB="`pwd`/test.db" $PYTHON cgi-bin/db/test_db.py
