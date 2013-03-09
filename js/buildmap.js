var map = new L.Map('map');
var idx = 1;
var features = [];

var url = 'http://a.tiles.mapbox.com/v3/tinybike.map-tvmjh342/{z}/{x}/{y}.png';
var osm = new L.TileLayer(url, {maxZoom: 18});

map.setView(new L.LatLng(30, 0), 2).addLayer(osm);
L.control.scale().addTo(map);
