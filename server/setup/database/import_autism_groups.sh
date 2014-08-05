#!/bin/sh
#import autism support group data

# Set ~/.pgpass for automated password entry
# see https://wiki.postgresql.org/wiki/Pgpass

set -e

DB_NAME=gov2014db
DB_USER=postgres
TABLE_NAME=autism_support_groups
SHAPEFILE=Autism/Aut_support.shp
SQL_FILE="$(mktemp)"

shp2pgsql -s 4326 $SHAPEFILE $TABLE_NAME $DB_NAME > $SQL_FILE
#more $SQL_FILE
psql $DB_NAME $DB_USER < $SQL_FILE
