function drawIconify(lat, lng, place_name, sick_words, population) {
	var IconifyCoords = new L.LatLng(parseFloat(lat), parseFloat(lng));
	var rescale = 10 + 25 / (1 + Math.exp(-0.4 * (sick_words - 20)));
	var mapIcon = L.icon({iconUrl: 'images/sadface.png', iconSize: [rescale, rescale]});
    var popupText = '<table><caption><h4>' + place_name + '</h4></caption><tr><td>Words:</td><td>' + sick_words + '</td></tr><tr><td>Pop. (2010):</td><td>' + population + '</td></tr><tr><td>Words/million people:</td><td>' + Math.round(1000000*sick_words/population*100)/100 + '</td></tr></table>';
	L.marker(IconifyCoords, {icon: mapIcon}).addTo(map).bindPopup(popupText);
}

function drawCircle(mapCircle) {
    var circleCoords = new L.LatLng(parseFloat(mapCircle[0]), parseFloat(mapCircle[1]));
    var circleOptions = {color: '#fff', opacity: 0.5, radius: 5, clickable: false};
	var circle = new L.CircleMarker(circleCoords, circleOptions);
	map.addLayer(circle);
}
