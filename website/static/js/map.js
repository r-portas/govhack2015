
var map = L.map('map').setView([lat, lng], 13);

var data = null;
var markers = [];

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: '',
    accessToken: ''
}).addTo(map);

$.ajax({
  url: $SCRIPT_ROOT + "/api/" + suburb,
  datatype: "jsonp",
  success: function(results){
    data = results;
    populate_map();
  }
});

//L.AwesomeMarkers.Icon.prototype.options.prefix = 'ion';

var hosMarker = L.AwesomeMarkers.icon({
  icon: "heart",
  markerColor: "red"
});

var busMarker = L.AwesomeMarkers.icon({
  icon: "bus",
  markerColor: "blue",
  prefix: 'fa'
});

function populate_map(){
  for (var i = 0; i < data["hospitals"].length; i++){
    hospital = data["hospitals"][i];
    var marker = L.marker([hospital["lat"], hospital["lng"]], {icon: hosMarker}).addTo(map);
    marker.bindPopup(hospital["name"]);

    markers.push(marker);
  }

  for (var i = 0; i < data["bus_stops"].length; i++){
    bus_stop = data["bus_stops"][i];
    var marker = L.marker([bus_stop[0], bus_stop[1]], {icon: busMarker}).addTo(map);
    markers.push(marker);
  }

}
