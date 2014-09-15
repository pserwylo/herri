if ( typeof Herri === 'undefined' ) { Herri = {}; }

Herri.Server = function() {

	var self = this;

	var loadDataLayer = function( map, type, params, callback ) {
		var path = "/api/geo/" + type;
		$.ajax({
			type: "GET",
			url: path,
			dataType: 'json',
			data: params,
			success: callback
		});
	};

	self.loadRegionGeometry = function( map, params, callback ) {
		loadDataLayer( map, 'region', params, callback );
	};

	self.loadPOIs = function( map, params, callback ) {
		loadDataLayer( map, 'poi', params, callback );
	};

};

Herri.RegionStyle = function( indexModel ) {

	var self = this;

	self.highlightHighest = false;

	self.getColourScale = function () {
		var colours = {
			green: ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837'],
			red: ['#ffeeee', '#ffeeee', '#fee0d2', '#fc9272', '#de2d26']
		};

		return colours.red;
	};

	self.getRegionStyle = function( feature ) {

		var lgaCode = feature.properties[ 'lga_code' ];
		var hasIndexModel = indexModel != null;
		var indexValue = hasIndexModel && indexModel.contains( lgaCode ) ? indexModel.getValue( lgaCode ) : null;
		var isHighest = self.highlightHighest && indexModel.isInHighest( lgaCode );

		var getColor = function() {

			if ( !hasIndexModel ) {
				// Haven't loaded the values for colourising yet. Set to white, and wait until
				// we get back here after loading the model results (at which point we will be
				// able to actually colourise the values).
				return '#ffffff';
			} else if ( indexValue == null ) {
				// Hrmm, that is odd. Why do we have an LGA on the map, without a corresponding
				// value in the index model?
				return '#ff0000';
			}

			if ( isHighest ) {
				return '#4444ff';
			}

			var colourList = self.getColourScale();
			if (indexValue < indexModel.getQuantile( 1 ) ) {
				return colourList[0];
			}
			else if (indexValue < indexModel.getQuantile( 2 ) ) {
				return colourList[1];
			}
			else if (indexValue < indexModel.getQuantile( 3 ) ) {
				return colourList[2];
			}
			else if (indexValue < indexModel.getQuantile( 4 ) ) {
				return colourList[3];
			}
			else {
				return colourList[4];
			}
		};


		return {
			fillColor: getColor( feature.properties ),
			weight: 2,
			opacity: 1,
			color: "#ffffff",
			dashArray: '3',
			fillOpacity: 0.7
		};
	};


};

/**
 * Rather than passing the model values through with the geometry from the server,
 * we instead fetch them separately. This allows us to send through geometry
 * without anything that is specific to the model we are viewing. This in turn allows
 * heavy caching of the geometry, both server and client side.
 * The catch is, we need to remember to restyle the geometry each time we receive
 * some more from the server (by calling restyleIndexLayer()
 */
Herri.IndexModel = function( modelId, modelDetails, modelData ) {

	var self = this;

	self.getId = function() { return modelId; };
	self.getDetails = function() { return modelDetails; };
	self.getName = function() { return modelDetails.name; };
	self.getDescription = function() { return modelDetails.description; };
	self.contains = function( lgaCode ) { return modelData.hasOwnProperty( lgaCode ); };
	self.getValue = function( lgaCode ) { return modelData[ lgaCode ]; };
	self.isInHighest = function( lgaCode ) { return highestIndexModelValues.hasOwnProperty( lgaCode ); };

	self.getQuantile = function( number ) {
		if ( number == 1 ) {
			return modelDetails[ 'quantile_1' ];
		} else if ( number == 2 ) {
			return modelDetails[ 'quantile_2' ];
		} else if ( number == 3 ) {
			return modelDetails[ 'quantile_3' ];
		} else if ( number == 4 ) {
			return modelDetails[ 'quantile_4' ];
		} else {
			throw new Error( "Unknown quantile " + number + ". Must be either 1, 2, 3, or 4." );
		}
	};

	var toHighlight = 5;
	var highestIndexModelValues = {};

	// Find the highest LGA's in the model, for highlighting purposes
	for ( var key in modelData ) {
		var value = modelData[ key ];
		if ( Object.keys( highestIndexModelValues ).length < toHighlight ) {
			highestIndexModelValues[ key ] = value;
		} else {
			// Iterate over each of the highest we have found so far and get
			// the lowest of them.
			var currentMinValue = Number.MAX_VALUE;
			var currentMinKey = null;
			for ( var k in highestIndexModelValues ) {
				if ( highestIndexModelValues[ k ] < currentMinValue ) {
					currentMinValue = highestIndexModelValues[ k ];
					currentMinKey = k;
				}
			}

			// Then we remove the lowest value, and replace it with the one
			// we just found to be higher than it...
			if ( currentMinValue < value ) {
				delete highestIndexModelValues[ currentMinKey ];
				highestIndexModelValues[ key ] = value;
			}
		}
	}

};

Herri.Map = function( server, indexModel ) {

	var self = this;
	var style = new Herri.RegionStyle( indexModel );
	var map = null;
	var layerToggles = null;
	var indexLayer = null;
	var regionLabelLayer = null;
	var mapBounds = null;
	var basemap = new Herri.BaseMap.OSM();

	// For debugging, it is helpful to expose this so that we can access it from the console.
	self._map = null;
	self._layerToggles = null;

	self.setBounds = function( b ) {
		mapBounds = b;
		return self;
	};

	self.setBaseMap = function( b ) {
		basemap = b;
		return self;
	};

	var createLegend = function() {

		//Code for the legend in the bottom right of the corner
		var legend = L.control( { position : 'bottomright' } );

		legend.onAdd = function () {

			var div = L.DomUtil.create( 'div', 'info legend' ),
					grades = [ 'Lowest', 'Low', 'Medium', 'High', 'Highest' ],
					colour = style.getColourScale();

			// loop through our density intervals and generate a label with a colored square for each interval
			div.innerHTML += '<ul>';
			for (var i = 0; i < grades.length; i++) {
				div.innerHTML +=
						'<li><div class="legendBox" style="background:' + colour[i] + '"></div> ' + '<div class="legendText">' + grades[i] + '</div></li>';
			}
			div.innerHTML += '</ul>';

			return div;
		};

		return legend;
	};

	var restyleIndexLayer = function() {
		if ( indexLayer != null ) {
			indexLayer.setStyle( style.getRegionStyle );
		}
	};

	var initialiseModel = function() {

		self.loadIndexLayer();

		if ( indexModel.getId() == 1 ) {
			self.loadServiceLayer( map, indexModel.getId() );
		}

		showModelDetails();
	};


	var showModelDetails = function() {

		if ( indexModel != null ) {
			restyleIndexLayer();
			$( '#modelName' ).html( indexModel.getName() );
			$( '#modelDescription' ).html( indexModel.getDescription() );
		}

	};

	// Keep track of the requests which are made. That way, if we are zooming in, and requesting
	// progressively more detailed geometry, we don't want to accidentally replace our nice fine
	// geometry with cruddy stuff from a previous (out of order) request.
	var indexLayerRequest = 0;
	var indexLayerResponse = 0;
	var indexLayerPreviousZoom = null;
	var indexLayerPreviousBounds = null;

	var removeOverlappingLabels = function() {

		var boundsOfKeptLabels = [];
		$( '#map').find( '.leaflet-label' ).each( function( j, item ) {

			var bounds = item.getBoundingClientRect();
			var overlap = false;

			for ( var ii = 0; ii < boundsOfKeptLabels.length; ii ++ ) {

				var i = boundsOfKeptLabels[ ii ];

				var withinX =
						( bounds.right > i.left && bounds.right < i.right ) ||
						( bounds.left > i.left && bounds.left < i.right );
				var withinY =
						( bounds.bottom > i.top && bounds.bottom < i.bottom ) ||
						( bounds.top > i.top && bounds.top < i.bottom );

				if ( withinX && withinY ) {
					overlap = true;
					break;
				}

			}

			if ( overlap ) {
				console.log( "Overlap. Poo" );
				$( this ).hide();
			} else {
				boundsOfKeptLabels.push( bounds );
			}

		});

	};

	self.loadIndexLayer = function() {

		/**
		 * When we send a request, we want to do two things:
		 *  - Request a little extra space (so that when we pan, we don't immediately need
		 *    to hit the server for more data
		 *  - Round the numbers to something more whole, so that we have opportunities to
		 *    cache responses and reuse in the future. For example, if you request bounds with
		 *    a west value of 5.531 or 5.582, clamping both to the value of 5.5 means that
		 *    they'd both require the same response, which is hopefully cached.
		 */
		var boundsToRequest = function() {

			var padBounds = function(xpad, ypad, xround, yround) {

				var bounds = map.getBounds();

				var west = bounds.getWest() - xpad;
				var east = bounds.getEast() + xpad;
				var north = bounds.getNorth() + ypad;
				var south = bounds.getSouth() - ypad;

				west -= west % xround;
				east -= east % xround + xround;
				north -= north % yround + yround;
				south -= south % yround;

				return L.latLngBounds( [ south, west ], [ north, east ] )
			};

			var zoomLevel = map.getZoom();

			/*
			 * TODO: Could probably do with some tuning here.
			 * Specifically, the rounding should be increased, to make it more
			 * likely that two requests want the same geometry. Right now, panning
			 * around still results in quite a few uncached requests to the server
			 * which is fairly slow.
			 */
			if ( zoomLevel <= 4 ) {
				return map.getBounds();
			} else if ( zoomLevel == 5 ) {
				return padBounds( 10, 8, 5, 4 );
			} else if ( zoomLevel == 6 ) {
				return padBounds( 3, 3, 1.5, 1.5 );
			} else if ( zoomLevel == 7 ) {
				return padBounds( 3, 2, 1, 1 );
			} else if ( zoomLevel == 8 ) {
				return padBounds( 2.5, 1.5, 1, 1 );
			} else {
				return padBounds( 2.2, 1.2, 1, 1 );
			}
		};

		var calcSimplificationThreshold = function(zoomLevel) {
			if ( zoomLevel <= 4 ) {
				return 0.22;
			} else if ( zoomLevel <= 5 ) {
				return 0.08;
			} else if ( zoomLevel <= 6 ) {
				return 0.06;
			} else if ( zoomLevel <= 8 ) {
				return 0.025;
			} else if ( zoomLevel <= 9 ) {
				return 0.01;
			} else if ( zoomLevel <= 10 ) {
				return 0.007;
			} else if ( zoomLevel <= 11 ) {
				return 0.005;
			} else {
				return 0.001;
			}
		};

		var data = {
			simplification_threshold : calcSimplificationThreshold( map.getZoom() )
		};

		var requestedBounds = boundsToRequest();

		// Zoom level 4 includes the whole country, so don't bother restricting.
		if ( map.getZoom() > 4 ) {
			data.xmin  = requestedBounds.getWest();
			data.ymin  = requestedBounds.getSouth();
			data.xmax  = requestedBounds.getEast();
			data.ymax  = requestedBounds.getNorth();
		}

		if ( indexLayerPreviousZoom != null ) {
			if ( indexLayerPreviousZoom == map.getZoom() &&
					indexLayerPreviousBounds.contains( map.getBounds() ) ) {
				console.log( "Not requesting data, because we are within the previous request" );
				return;
			}
		}

		var layerRequest = indexLayerRequest;
		indexLayerRequest ++;

		var oldZoom = map.getZoom();
		var oldBounds = requestedBounds;

		server.loadRegionGeometry( map, data, function (response) {

			// Discard incoming layers that are superseded by a newer request
			if ( layerRequest == indexLayerResponse ) {
				if ( indexLayer != null ) {
					console.log( "Removing previous index layer from map." );
					map.removeLayer( indexLayer );
				}

				if ( regionLabelLayer == null ) {
					regionLabelLayer = L.layerGroup();
					regionLabelLayer.addTo( map );
					layerToggles.addOverlay( regionLabelLayer, 'Region names' );
				} else {
					regionLabelLayer.clearLayers();
				}

				var eachFeature = function( feature, layer ) {

					var name = feature.properties.name;

					if (feature.geometry.coordinates.length == 0 ) {
						console.log( "Feature has no coordinates:" );
						console.log( feature );
						return layer;
					}

					var iconOptions = {
						className : 'region-label'
					};

					var markerOptions = {
						icon: new L.DivIcon( iconOptions )
					};

					var markerCenter = layer.getBounds().getCenter();

					var marker = L.marker( markerCenter, markerOptions );

					var labelOptions = {
						noHide : true,
						offset : [ -47.5, -15 ] // Average width of labels is about 95px wide for Victoria.
					};

					marker.bindLabel( name, labelOptions ).addTo( regionLabelLayer );
					return layer;
				};

				console.log("Adding index layer to map.");
				indexLayer = L.geoJson(response, {
					style: style.getRegionStyle,
					onEachFeature: eachFeature
				}).addTo(map);

				// Now that we've added the labels to the map, they should all have dom elements
				// that we can interrogate regarding size and position. We'll take the opportunity
				// to find overlapping ones, and hide them.
				removeOverlappingLabels();

				// Store the cached versions from before the response was sent, because the user may
				// have interacted with the map since then.
				indexLayerPreviousZoom = oldZoom;
				indexLayerPreviousBounds = oldBounds;

			}
			indexLayerResponse ++;

		});
	};

	var onZoomEnd = function() {
		self.loadIndexLayer();
	};

	var onPanEnd = function() {
		self.loadIndexLayer();
	};

	self.loadServiceLayer = function( map ) {

		var popupOptions = {
			className: "poi-info"
		};

		var initPopup = function( feature, layer ) {
			if ( feature.properties && feature.properties.name ) {
				var html =
					"<div class='name'>" + feature.properties.name + "</div>" +
					"<p>" + feature.properties.description + "</p>";
				layer.bindPopup( html, popupOptions );
			}
		};

		server.loadPOIs( map, {}, function (response) {

			var layer   = L.geoJson(
				response,
				{
					style: style,
					onEachFeature : initPopup
				}
			).addTo(map);

			layerToggles.addOverlay( layer, 'Support Groups' );

		});

	};

	self.init = function( initialView, defaultZoom, minZoom ) {

		map = self._map = L.map('map', {
			maxBounds : mapBounds,
			minZoom : minZoom
		}).setView( initialView, defaultZoom );

		basemap.createTileLayer( minZoom ).addTo( map );
		createLegend().addTo( map );

		var dummyLayer = L.polygon([], {});
		var toggles = { 'Highest value' : dummyLayer };
		var options = { collapsed : false };

		layerToggles = self._layerToggles = L.control.layers( {}, toggles, options ).addTo( map );
		map.on( 'overlayadd', function( event ) {
			if ( dummyLayer == event.layer ) {
				style.highlightHighest = true;
				restyleIndexLayer();
			} else if (regionLabelLayer == event.layer) {
				removeOverlappingLabels();
			}
		}).on( 'overlayremove', function( event ) {
			if ( dummyLayer == event.layer ) {
				style.highlightHighest = false;
				restyleIndexLayer();
			}
		});

        map.on( 'zoomend', onZoomEnd );
        map.on( 'dragend',  onPanEnd  );

		initialiseModel();

		return self;

	};

};

Herri.BaseMap = function( url, parameters ) {

	var self = this;

	self.createTileLayer = function( minZoom ) {
		parameters.minZoom = minZoom;
		parameters.maxZoom = 14;
		return L.tileLayer( url, parameters );
	};

};

Herri.BaseMap.MapBox = function( mapboxId ) {

	var self = this;

	var getUrl = function() {
		return 'https://{s}.tiles.mapbox.com/v3/' + mapboxId + '/{z}/{x}/{y}.png';
	};

	var getAttribution = function() {
		return 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>';
	};

	Herri.BaseMap.call( this, getUrl(), { attribution : getAttribution() } );

};

Herri.BaseMap.OSM = function() {

	var self = this;

	var getUrl = function() {
		return 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	};

	var getAttribution = function() {
		return 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	};

	Herri.BaseMap.call( this, getUrl(), { attribution : getAttribution() } );

};