function drawIconify(lat, lng, city_name, sick_words) {
	var IconifyCoords = new L.LatLng(parseFloat(lat), parseFloat(lng));
	var mapIcon = L.icon({iconUrl: 'images/sadface.png', iconSize: [25, 25]});
    var popupText = '<center>' + city_name + ': ' + sick_words + '</center>';
	L.marker(IconifyCoords, {icon: mapIcon}).addTo(map).bindPopup(popupText);
}

function drawCircle(mapCircle) {
    var circleCoords = new L.LatLng(parseFloat(mapCircle[0]), parseFloat(mapCircle[1]));
    var circleOptions = {color: '#fff', opacity: 0.5, radius: 5, clickable: false};
	var circle = new L.CircleMarker(circleCoords, circleOptions);
	map.addLayer(circle);
}
