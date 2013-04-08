var map = new L.Map('map');
var idx = 1;
var features = [];

var url = 'http://a.tiles.mapbox.com/v3/tinybike.map-tvmjh342/{z}/{x}/{y}.png';
var osm = new L.TileLayer(url, {maxZoom: 18});

map.setView(new L.LatLng(43, -110), 4).addLayer(osm);
L.control.scale().addTo(map);

// Generate heatmap layer (requires heatmap.js and heatmap-leaflet.js)
var heatmapLayer = L.TileLayer.heatMap({
		radius: 20,
		opacity: 0.8,
		gradient: {
			0.45: 'rgb(0,0,255)',
			0.55: 'rgb(0,255,255)',
			0.65: 'rgb(0,255,0)',
			0.95: 'yellow',
			1.0: 'rgb(255,0,0)'
		}
	});
	
var testData = {
	max: 46,
	data: [
		{lat: 33.5363, lon: -117.044, value: 1}, 
		{lat: 33.5608, lon: -117.24, value: 1}
	]
};

heatmapLayer.addData(testData.data);
 
var overlayMaps = {'Heatmap': heatmapLayer};
 
var controls = L.control.layers(null, overlayMaps, {collapsed: false});
 
var map = new L.Map('heatmapArea', {
	center: new L.LatLng(51.505, -0.09),
	zoom: 6,
	layers: [baseLayer, heatmapLayer]
});
 
controls.addTo(map);
 
// Make heatmap accessible for debugging
// layer = heatmapLayer;