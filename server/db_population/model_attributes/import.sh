#!/bin/sh

# Set ~/.pgpass for automated password entry
# see https://wiki.postgresql.org/wiki/Pgpass

DB_USER=django
DB=django

echo "TRUNCATE api_attribute CASCADE;" | psql -w $DB $DB_USER
psql -w $DB $DB_USER < api_attribute.sql
