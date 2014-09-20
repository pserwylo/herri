# Model Attributes

As herri gets developed, we will add more attributes from the census to this file ready for importing.
Ideally, there will be a nice spruced up admin interface for people to do this, but for now, it is still
a pretty manual import process.

The command to dump the table is:

pg_dump -U $DB_USER --table api_attribute --data-only
