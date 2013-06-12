// JavaScript Document
/*$(function() {
$( "#CompPerBeginDate" ).datepicker();
});
*/
var request;
if (window.XMLHttpRequest) {
	request = new XMLHttpRequest();
} else {
	request = new ActiveXObject("Microsoft.XMLHTTP");
}
request.open('GET', '/app/api/v1/report/?format=json');
request.onreadystatechange = function() {
	if ((request.readyState===4) && (request.status===200)) {
		var items = JSON.parse(request.responseText);
		var output;
		for (var key in items) {
			output += '<h3><strong>Violation: </strong>' + items[key].pws_affected.name + '</h3><div><ul id="moreinfo"><li>County: '  + items[key].pws_affected.county + '</li><li>Compliance Monitoring Start Date: ' + items[key].date_reported + '</li><li>Contaminant Name: '  + items[key].contaminant_name + '</li><li>Violation Summary: '  + items[key].summary + '</li><li>Populationn Served: '  + items[key].pws_affected.population_served + '</li><li>Status: '  + items[key].pws_affected.status + '</li><li>Contact : <br />'  + items[key].pws_affected.contact_name + '<br />' + items[key].pws_affected.contact_addr1 + '<br />'  + items[key].pws_affected.contact_city + ', '  + items[key].pws_affected.contact_state + ' '  + items[key].pws_affected.contact_zip + '</li></ul><p>Download in-depth report: (<a href="#">pdf</a>|<a href="#">doc</a>|<a href="#">txt</a>|<a href="#">tex</a>)</p></div>';
		}
		document.getElementById('violation_enforcement_epa').innerHTML = output;
		$( "#violation_enforcement_epa" ).accordion();
	}
}
request.send();

// accordion listing
/*$(function() {
$( "#violation_enforcement_epa" ).accordion();
});
*/


// add a map to the system
function initialize() {
  if (GBrowserIsCompatible()) {
	var map = new GMap2(document.getElementById("map_canvas"));
	map.setCenter(new GLatLng(33.933106, --83.403397), 13);
	map.setUIToDefault();

	// Create a base icon for all of our markers that specifies the
	// shadow, icon dimensions, etc.
	var baseIcon = new GIcon(G_DEFAULT_ICON);
	baseIcon.shadow = "http://www.google.com/mapfiles/shadow50.png";
	baseIcon.iconSize = new GSize(20, 34);
	baseIcon.shadowSize = new GSize(37, 34);
	baseIcon.iconAnchor = new GPoint(9, 34);
	baseIcon.infoWindowAnchor = new GPoint(9, 2);

	// Creates a marker whose info window displays the letter corresponding
	// to the given index.
	function createMarker(point, index) {
	  // Create a lettered icon for this point using our icon class
	  var letter = String.fromCharCode("A".charCodeAt(0) + index);
	  var letteredIcon = new GIcon(baseIcon);
	  letteredIcon.image = "http://www.google.com/mapfiles/marker" + letter + ".png";

	  // Set up our GMarkerOptions object
	  markerOptions = { icon:letteredIcon };
	  var marker = new GMarker(point, markerOptions);

	  GEvent.addListener(marker, "click", function() {
		marker.openInfoWindowHtml("Marker <b>" + letter + "</b>");
	  });
	  return marker;
	}

	// Add 10 markers to the map at random locations
	var bounds = map.getBounds();
	var southWest = bounds.getSouthWest();
	var northEast = bounds.getNorthEast();
	var lngSpan = northEast.lng() - southWest.lng();
	var latSpan = northEast.lat() - southWest.lat();
	for (var i = 0; i < 10; i++) {
	  var latlng = new GLatLng(southWest.lat() + latSpan * Math.random(),
		southWest.lng() + lngSpan * Math.random());
	  map.addOverlay(createMarker(latlng, i));
	}
  }
}