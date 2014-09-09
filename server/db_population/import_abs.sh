#!/bin/sh
#import abs data

# Set ~/.pgpass for automated password entry
# see https://wiki.postgresql.org/wiki/Pgpass

DB_USER=django
DB=django

psql -w $DB $DB_USER < b01.sql
psql -w $DB $DB_USER < b04a.sql
psql -w $DB $DB_USER < b04b.sql
psql -w $DB $DB_USER < b11a.sql
psql -w $DB $DB_USER < b11b.sql
psql -w $DB $DB_USER < b13.sql
psql -w $DB $DB_USER < b14.sql
psql -w $DB $DB_USER < b17b.sql
psql -w $DB $DB_USER < b21.sql
psql -w $DB $DB_USER < lga_attributes_all.sql
