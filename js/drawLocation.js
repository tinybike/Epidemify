function drawIconify(mapIconify, link) {
	var IconifyCoords = new L.LatLng(mapIconify[2], mapIconify[3]);
	var mapIcon = L.icon({iconUrl: 'images/icon.png', iconSize: [35, 35]});
    var popupText = '';
	L.marker(IconifyCoords, {icon: mapIcon}).addTo(map).bindPopup(popupText);
}

function drawCircle(mapCircle) {
    var circleCoords = new L.LatLng(parseFloat(mapCircle[1]), parseFloat(mapCircle[2]));
    var circleOptions = {color: '#fff', opacity: 0.5, radius: 5, clickable: false};
	var circle = new L.CircleMarker(circleCoords, circleOptions);
	map.addLayer(circle);
}
