<?php
// Connect to MySQL DB
function makeDBConnection() {
	
	if (!func_num_args()) {
		$db_host = 'localhost';
		$db_user = 'epidemician';
		$db_pass = 'funcrusherplus';
		$db_name = 'Epidemify';
	}
	else
		list($db_host, $db_user, $db_pass, $db_name) = func_get_args();

	$connection = mysqli_connect($db_host, $db_user, $db_pass);
	if (mysqli_connect_errno()) {
	    printf('Connect failed: %s\n', mysqli_connect_error());
	    exit();
	}
	if (isset($db_name)) {
		if (!mysqli_select_db($connection, $db_name)) {
			exit("Error: can't select database!");
		}
	}
	return $connection;
}

function dbSafe($connection, $value) {
	return '"' . mysqli_real_escape_string($connection, $value) . '"';
}
