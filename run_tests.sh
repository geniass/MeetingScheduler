#!/bin/bash

PYTHON="/usr/bin/env python3"

#./setup_db.sh

DB="`pwd`/test.db"
cd cgi-bin
TEST_DB=$DB $PYTHON -m tests.test_db
