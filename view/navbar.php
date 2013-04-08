<?php
function create_navbar($updated) {
	echo '
	<div id="topbar">
		<div id="nav">
			<nav>
			<div class="tabs_table">
				<table>
				<tr>
					<td onclick="window.location = \'index.php\';" style=\'cursor: hand; cursor: pointer;\'><a href="index.php">EPIDEMIFY</a></td>
					<div id="how">
					<td>
					<a id="how-trigger" href="#">HOW THIS WORKS</a>
					<div id="how-content">
						<small>
						<p>Epidemify is a tool for estimating where people are sick.  We parse the article, searching for occurrences of words associated with sickness (ailing, sick, illness, etc.), as well as names of places (our test data are the U.S. states and territories).  We then simply count the number of times any "sick words" appear in articles which also contain a place name.  The association resulting from this is then displayed on the map.  Click on a face and the popup will show you how many sick words were found at that location!</p><br />
						<p>This is a brand new tool, and we are still building our program -- this is just the most simple version!  Please come back regularly; there is plenty more to come.</p><br />
						<p><i>Epidemify was last updated on ' . $updated[1] . '/' . $updated[2] . '/' . $updated[0] . '.  All articles used were at most 30 days old.</i></p>
						</small>
					</div>
					</td>
					</div>
	';
	left_navbar();
	echo '
				</tr>
				</table>
			</div>
			</nav>
		</div><nav>';
	right_navbar();
	echo '
	</nav>
	</div>
	';
}

function left_navbar() {
	if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == TRUE) {
		echo '
		<td><a href="index.php?page=network"><small>network</small></a></td>
		<td><a href="index.php?page=profile"><small>profile</small></a></td>
		';
	}
}

function right_navbar() {
	if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == TRUE) {
		echo '
		<div class="tabs_table">
			<div class="tabs">
			<table>
				<tr>
				<td><a href="index.php?page=logout">LOGOUT</a></td>
				</tr>
			</table>
			</div>
		</div>
		';
	}
	else {
		echo '
		<div class="tabs_table">
			<div class="tabs">
				<table>
					<div id="login">
						<tr>
						<td>
							<a id="try-1" class="try" href="#">SIGN UP</a>								
						</td>
						<td>
							<a id="login-trigger" href="#">LOGIN</a>
							<div id="login-content">
								<form action="index.php?page=login" method="post" class="form">
									<fieldset id="inputs">
										<input id="username" type="username" name="login_username" placeholder="Username" required />
										<input id="password" type="password" name="login_password" placeholder="Password" required />
									</fieldset>
									<fieldset id="actions">
										<input class="button" type="submit" id="submit" value="Login" />
										<label><input type="checkbox" checked="checked" /> <small>Keep me signed in</small></label>
									</fieldset>
								</form>
							</div>
						</td>
						</tr>
					</div>
				</table>
			</div>
		</div>
		';
	}
}
