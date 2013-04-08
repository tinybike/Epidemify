<?php include 'view/navbar.php'; ?>
<!DOCTYPE html>
<html>
<head>
<title>Epidemify</title>
<?php include 'view/headers.html'; ?>
<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.4.4/leaflet.css" />
<script src="js/jquery.lightbox_me.js"></script>
<script src="js/mapbox.js"></script>
<script src="js/arc.js"></script>
<script src="http://cdn.leafletjs.com/leaflet-0.4.4/leaflet.js"></script>
<script src="js/heatmap.js"></script>
<script src="js/heatmap-leaflet.js"></script>
<script src="js/drawLocation.js"></script>
<script>
$(document).ready(function() {

	// Drop-down boxes
	$('#login-trigger').click(function() {
		$(this).next('#login-content').toggle();
		$(this).toggleClass('active');							
		if ($(this).hasClass('active')) {
			$(this).find('span').html('&#x25B2;');
		}
		else {
			$(this).find('span').html('&#x25BC;');
		}
	})
	$('#how-trigger').click(function() {
		$(this).next('#how-content').toggle();
		$(this).toggleClass('active');							
		if ($(this).hasClass('active')) {
			$(this).find('span').html('&#x25B2;');
		}
		else {
			$(this).find('span').html('&#x25BC;');
		}
	})

	// Signup lightbox
	$('#try-1').click(function(e) {
		$('#sign_up').lightbox_me({
			centered: true, 
			onLoad: function() { 
				$('#sign_up').find('input:first').focus()
				}
			});
		e.preventDefault();
	});

	// Search query
	$('#finder').submit(function() {
		$.post('index.php', $(this).serialize(), function(response) {
			$('#links').html(response);
		});
		return false;
	});

});

function selectLocation() {
    var location = [Lat, Lng];
    drawIconify(location, false);                
	$.post('index.php?page=network', {
			'lat': Lat,
			'lng': Lng,
		}, function(response) {
			$('#book').html(response);
		}
	);
}
</script>
</head>

<body>
<div class="wrapper">
	<?php create_navbar($updated); ?>
	<div id="map"></div>
	<script src="js/buildmap.js"></script>
	<?php
	foreach ($sick_map as $city) {
		echo '
		<script>
		drawIconify(' . $city['latitude'] . ', ' . $city['longitude'] . ', "' . $city['name'] . '", ' . $city['sick_words'] . ');
		</script>
		';
	}
	?>
	<div id="leftbar">
		<form action="index.php" method="post" class="form">
		<table>
		<tr><td>Location search</td></tr>
		<tr>
		<td><input id="origin" class="text_input" type="text" name="origin" size="15" required="required" placeholder="City or place name" /></td>
		<td><input class="button" type="submit" value="Search" /></td>
		</tr>
		</table>
		<table>
		<tr><td>Disease search</td></tr>
		<tr>
		<td><input id="origin" class="text_input" type="text" name="origin" size="15" required="required" placeholder="Disease name" /></td>
		<td><input class="button" type="submit" value="Search" /></td>
		</tr>
		</table>
		</form>
	</div>
	<div class="push"></div>
</div>
<div id="footer">&copy; <?php echo $updated[0]; ?> <a href="http://www.tinybike.net">Jack Peterson</a>.  All rights reserved.</div>

<!--- Sign-up lightbox --->
<div id="sign_up">
	<h3 id="see_id">Sign up</h3>
	<div id="sign_up_form">
		<form action="index.php?page=signup" method="post" class="form">
			<label><strong>Username:</strong> <input class="text_input" type="text" name="signup_username" size="25" autocomplete="off" required="required" /></label>
			<label><strong>Email:</strong> <input class="text_input" type="text" name="signup_email" size="25" autocomplete="off" required="required" /></label>
			<label><strong>First name:</strong> <input class="text_input" type="text" name="signup_firstname" size="25" autocomplete="off" required="required" /></label>
			<label><strong>Last name:</strong> <input class="text_input" type="text" name="signup_lastname" size="25" autocomplete="off" required="required" /></label>
			<label><strong>Password:</strong> <input class="text_input" type="password" name="signup_password" size="25" autocomplete="off" required="required" /></label>
			<div id="signup_actions">
				<input class="button" type="submit" id="signup_button" value="Create account" />
			</div>
		</form>
	</div>
</div>
<!--- end lightbox --->

</body>
</html>
