#!/bin/bash

DEV_DB="/var/www/development.db"

# apt-get install sqlite

sqlite3 $DEV_DB 'CREATE TABLE IF NOT EXISTS meetings_students(
    meeting_id          INTEGER NOT NULL REFERENCES meetings(id),
    student_id          INTEGER NOT NULL,
    PRIMARY KEY(meeting_id, student_id)
);'
sqlite3 $DEV_DB 'CREATE TABLE IF NOT EXISTS meetings(
    lecturer_id         TEXT NOT NULL,
    datetime            TIMESTAMP NOT NULL,
    duration            INTEGER NOT NULL,
    subject             TEXT
);'


chmod 660 $DEV_DB
chown www-data:www-data $DEV_DB
