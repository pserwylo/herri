[![Herri logo](https://raw.github.com/pserwylo/herri/master/docs/images/herri-logo-400px.png)](https://github.com/pserwylo/herri)

What is Herri?
==============

Herri (a Basque word for "commune") is a tool that facilitiates creating and sharing service cachment models.
Service cachement area models are models which allow a specific subset of the population to be modelled to see how prevailent they are in the community.
This information is then used in addition to information about the location of particular service providers and displayed on the same map.
The end result is a visual representation of where a population of interest resides, and if they are adequetly serviced by existing providers. 

[![Introductory video](https://raw.github.com/pserwylo/herri/master/docs/images/intro-video.png)](http://vimeo.com/100622218)

For example, the initial motivation for the project was to visualise where families that may desire autism support services live in Victoria, Australia.
This information is then crossreferenced with the current location of autism support services.
As a result, one is able to visualise where there is a lack of support for services, or where there is an oversupply.

In addition to the web application, we also worked hard during the hackathon to prototype a card/board game which will be used to help educate people without about the concepts involved, without using any computers.
The goal is to develop an app which uses image processing to turn a photograph of the physical board and convert it into an interactive model for people to explore. 

Demo
====

The first version (hacked together in 48hrs) is available at http://herri.serwylo.com. It is running of the code in the "govhack-2014-submission" tag.
In the future (after voting is closed), this will be updated to a newer version of herri.

Why was it created?
===================

Herri was created during GovHack 2014 - a 48h hackathon in Australia, where teams are encouraged to build awesome things with open government data. 
This project opted to make use of the census data, provided by the Australian Beauru of Statistics.

[GovHack 2014 project page](http://hackerspace.govhack.org/content/herri-find-your-place-your-community)

Who created it?
===============

The Herri team consisted of the following people:
 * Fred
 * Ben
 * Kim
 * Brad
 * Kane 
 * Lyndon
 * Daniel
 * Pete

Installing herri
================

Herri has a few moving parts that are involved, partly due to the fact that there are great tools which do most of the hard work for us, and partly due to the fact that the 48hr hackathon put a lot of pressure on us to just hack something together which worked. 
This section will document both herri itself, and each of its dependencies.

Installing on Ubuntu 14.04
--------------------------

sudo apt-get install apache2 postgresql-client-9.3 postgresql-9.3-postgis-2.1 gdal-bin

The dependencies are:
 * PostgreSQL + PostGIS (used by geodjango - spatialite may work but it is untested)
 * Apache2 (or some other webserver which works nicely with django)
 * GDAL/OGR (preprocessing geospatial files before importing)

Python dependencies
-------------------

 * psycopg2
 * vectorformats
 * simplejson<=2.0.7 (see https://github.com/simplejson/simplejson/issues/37 for biff between simplejson and django devs as to why latest is not suitable)

PostgreSQL setup
----------------

su postgres
createuser -P <username>
createdb <database_name>

# http://postgis.net/docs/postgis_installation.html#install_short_version
psql -d <database_name> -c "CREATE EXTENSION postgis;"

cp herri/local_settings.py.example herri/local_settings.py
# Edit local_settings.py and specify relevant database settings (username, password, database name)

# Ask django to create relevant tables for us.
python {path/to/manage.py}/manage.py syncdb

Importing data
--------------

Cencus data:
 * Visit https://www.censusdata.abs.gov.au/datapacks/DataPacks?release=2011 (account required)
 * Download "Local Government Areas" for all of Australia
 * Unzip "2011_BCP_LGA_for_AUST_short-header.zip" file
 * `mv "2011 Census BCP Local Government Areas for AUST/AUST/*" server/db_population/census2011/`
 * cd server/db_population/
 * `./import_abs.sh`

Local Government Areas (LGAs): 
 * Visit http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1259.0.30.001July%202011?OpenDocument
 * Download "Local Government Area ASGC Ed 2011 Digital Boundaries in ESRI Shapefile Format"
 * Unzip the file to db_population/LGAs
 * cd to server/db_population/LGAs
 * run `./prepare.sh` (to filter out areas with a size of 'null' that cause import errors)
 * cd to server/herri
 * Open the django shell: `python manage.py shell`
 * From the shell, run:
 ** from api import load
 ** load.load_lga()

Autism support groups:
 * Open the django shell: `python manage.py shell`
 * From the shell, run:
 ** from api import load
 ** load.load_autism_poi()
 ** load.create_or_update_autism_model()

TODO: Explain the config files for the relevant software.

Contributing to herri
=====================

With an application such as Herri, there is always opportunity to improve. 
Whether it is improving accessibility for people without computers, people with disabilities or people with mobile devices.
Perhaps you have an interesting dataset that would be useful to integrate and allow others to make awesome models.

Feel free to contribute by visiting the GitHub issue tracker and seeing what is required, or adding your own issues.
