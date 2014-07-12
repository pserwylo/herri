#!/bin/sh
#import abs data

# Set ~/.pgpass for automated password entry
# see https://wiki.postgresql.org/wiki/Pgpass

DB_USER=postgres
DB=gov2014db

psql -w $DB $DB_USER < b17b.sql
