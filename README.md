[![Herri logo](https://raw.github.com/pserwylo/herri/master/docs/images/herri-logo-400px.png)](https://github.com/pserwylo/herri)

# What is Herri?

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

## Demo

The first version (hacked together in 48hrs) is available at http://herri.serwylo.com. It is running of the code in the "govhack-2014-submission" tag.
In the future (after voting is closed), this will be updated to a newer version of herri.

## Why was it created?

Herri was created during GovHack 2014 - a 48h hackathon in Australia, where teams are encouraged to build awesome things with open government data. 
This project opted to make use of the census data, provided by the Australian Beauru of Statistics.

[GovHack 2014 project page](http://hackerspace.govhack.org/content/herri-find-your-place-your-community)

## Who created it?

The Herri team consisted of the following people:
 * Fred
 * Ben
 * Kim
 * Brad
 * Kane 
 * Lyndon
 * Daniel
 * Pete

# Installing herri

Herri has a few moving parts that are involved, partly due to the fact that there are great tools which do most of the hard work for us, and partly due to the fact that the 48hr hackathon put a lot of pressure on us to just hack something together which worked. 
This section will document both herri itself, and each of its dependencies.

## Installing on Ubuntu 14.04

`sudo apt-get install apache2 postgresql-client-9.3 postgresql-9.3-postgis-2.1 gdal-bin pgxnclient postgresql-server-dev-9.3`

The dependencies are:
 * PostgreSQL + PostGIS (used by geodjango - spatialite may work but it is untested)
 * Apache2 (or some other webserver which works nicely with django)
 * GDAL/OGR (preprocessing geospatial files before importing)
 * PGXN (package manager for PostgreSQL - used to install the "quantile" extension for PostGIS. This is also why postgresql-server-dev-9.3 is required, in order to build the quantile extension)

## Python dependencies

 * psycopg2
 * vectorformats
 * simplejson<=2.0.7 (see https://github.com/simplejson/simplejson/issues/37 for biff between simplejson and django devs as to why latest is not suitable)
 * wadofstuff-django-serializers

Troubleshooting "Could not find any downloads that satisfy the requirement wadofstuff-django-serializers"

Your pip installation may refuse to install wadofstuff, because the package maintainers don't host it on pypi.org. Even if you `pip --allow-external`, then it can fail because they only have a http:// link, not a https:// link. This can be gotten around by giving pip the https link to download: `pip install https://wadofstuff.googlecode.com/files/wadofstuff-django-serializers-1.1.0.tar.gz`.

## PostgreSQL setup

* `su postgres`
* `createuser -P <username>`
* `createdb <database_name>`
* `psql -d <database_name> -c "CREATE EXTENSION postgis;"` (http://postgis.net/docs/postgis_installation.html#install_short_version)

### Install the "quantile" extension:

* `pgxn load -d <database_name> quantile`

#### Install "quantile" extension (MANUALLY)

In theory, pgxn should be able to do this for us.
In practice, it hasn't worked the previous two times a herri server was setup.
If the  previous pgxn command doesn't work, then you can install it manually:

* `cd /tmp`
* `wget http://api.pgxn.org/dist/quantile/1.1.3/quantile-1.1.3.zip`
* `unzip quantile-1.1.3.zip`
* `cd quantile`
* `make`
* `make install` (as root user)
* `psql <database_name> -c "CREATE EXTENSION quantile"` (as postgres user)

# Configuring Herri

The settings which are specific to your site are in a file named 'local_settings.py'.
To create this file, `cp herri/local_settings.py.example herri/local_settings.py`. 
Then edit local_settings.py and specify relevant database settings (username, password, database name)

After doing so, ask django to create relevant tables for us `python manage.py syncdb`.

## Importing data

### Census data (TableBuilder)

TableBuilder is a more customized way to decide what census data to get out of the ABS.
Right now, the process for importing it is a little shonky, but bear with us until a proper import routine is setup:

Firstly, we need a table "b01_aust_lga_short" present, which has a field "tot_p_p" in it. 
This is neccesary because we need to be able to normalise index models based on LGA's total population.
The reason for the b01_aust_lga_short table is because historically it is information that we had handy, and so we may as well use it. 

 * See "Census data (DataPacks)" below for instructions on how to get the census data.
 * `cd server/db_populations`
 * `psql -w <db_name> <db_user> < b01.sql`

Once the b01 table is in the database, then we can actually import the table builder data:

 * `python manage.py shell`
 * `from api import load`
 * `load.TableBuilder('/census-table-builder/Tablebuildercompilation.csv').load()`

### Census data (DataPacks)

DataPacks are the way in which the ABS packages up data to be donwloaded.
They come ready with various attributes, which may or may not be desirable for you.

 * Visit https://www.censusdata.abs.gov.au/datapacks/DataPacks?release=2011 (account required)
 * Download "Local Government Areas" for all of Australia
 * Unzip "2011_BCP_LGA_for_AUST_short-header.zip" file
 * `mv "2011 Census BCP Local Government Areas for AUST/AUST/*" server/db_population/census2011/`
 * `cd server/db_population/`
 * setup the database name variable in the import_abs.sh 
 * `./import_abs.sh`

### Local Government Areas (LGAs)

 * Visit http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1259.0.30.001July%202011?OpenDocument
 * Download "Local Government Area ASGC Ed 2011 Digital Boundaries in ESRI Shapefile Format"
 * Unzip the file to db_population/LGAs
 * `cd to server/db_population/LGAs`
 * run `./prepare.sh` (to filter out areas with a size of 'null' that cause import errors)
 * `cd server/herri/`
 * Open the django shell: `python manage.py shell`
 * From the shell, run:
   * `from api import load`
   * `load.load_lga()`

### Autism support groups

 * Open the django shell: `python manage.py shell`
 * From the shell, run:
   * `from api import load`
   * `load.load_autism_poi()`
   * `load.create_or_update_autism_model()`

TODO: Explain the config files for the relevant software.

# Contributing to herri

With an application such as Herri, there is always opportunity to improve. 
Whether it is improving accessibility for people without computers, people with disabilities or people with mobile devices.
Perhaps you have an interesting dataset that would be useful to integrate and allow others to make awesome models.

Feel free to contribute by visiting the GitHub issue tracker and seeing what is required, or adding your own issues.
