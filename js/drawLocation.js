function drawIconify(lat, lng, city_name, sick_words) {
	var IconifyCoords = new L.LatLng(parseFloat(lat), parseFloat(lng));
	var rescale = 10 + 25 / (1 + Math.exp(-0.4 * (sick_words - 20)));
	var mapIcon = L.icon({iconUrl: 'images/sadface.png', iconSize: [rescale, rescale]});
    var popupText = '<center>' + city_name + ': ' + sick_words + '</center>';
	L.marker(IconifyCoords, {icon: mapIcon}).addTo(map).bindPopup(popupText);
}

function drawCircle(mapCircle) {
    var circleCoords = new L.LatLng(parseFloat(mapCircle[0]), parseFloat(mapCircle[1]));
    var circleOptions = {color: '#fff', opacity: 0.5, radius: 5, clickable: false};
	var circle = new L.CircleMarker(circleCoords, circleOptions);
	map.addLayer(circle);
}
