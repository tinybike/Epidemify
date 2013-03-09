<?php
function create_navbar() {
	echo '
	<div id="topbar">
		<div id="nav">
			<div class="tabs_table">
				<table>
				<tr>
					<td><a href="index.php">epidemify</a></td>
	';
	left_navbar();
	echo '
				</tr>
				</table>
			</div>
		</div>		
		<nav>';
	right_navbar();
	echo '
	</nav>
	</div>
	';
}

function left_navbar() {
	if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == TRUE) {
		echo '
		<td><a href="index.php?nb=network"><small>network</small></a></td>
		<td><a href="index.php?nb=profile"><small>profile</small></a></td>
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
				<td><a href="index.php?nb=logout">log out</a></td>
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
							<a id="try-1" class="try" href="#">sign up</a>								
						</td>
						<td>
							<a id="login-trigger" href="#">log in</a>
							<div id="login-content">
								<form action="index.php?nb=login" method="post" class="form">
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
