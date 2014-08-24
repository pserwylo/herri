#!/bin/bash

SOURCE=LGA_2011_AUST.shp

if [ -d filtered ]
then
	echo "Removing previously filtered data..."
	rm -r filtered
fi

if [ -e $SOURCE ]
then
	echo "Filtering out features with 'null' area..."
	mkdir filtered
	ogr2ogr \
		-f "ESRI Shapefile" \
		-where "AREA_SQKM is not null" \
		filtered/$SOURCE \
		$SOURCE
else
	echo "You don't seem to have the relevant LGA shapefiles downloaded (LGA_2011_AUST)."
	echo "They can be downloaded from:"
	echo " * http://www.abs.gov.au/ausstats/abs@.nsf/mf/1259.0.30.001"
	echo " * [or direct link - http://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1259030001_lga11aaust_shape.zip&1259.0.30.001&Data%20Cubes&03275B7661181087CA2578CC001223EA&0&July%202011&14.07.2011&Latest]"
fi

