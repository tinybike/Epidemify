<?php
class Model {

	public function signup($user) {
		/*
		Return values:
		0 = success
		1 = required fields not filled out
		2 = password too short
		3 = username already taken
		4 = database write error
		*/ 
		// If there are any required fields not filled out, send the user back to the form
		$required = array('signup_username', 'signup_password', 'signup_email', 'signup_firstname', 'signup_lastname');
		foreach ($required as &$value) {
			if ($user[$value] == '')
				return 1;
		}
		$username = $user['signup_username'];
		$password = $user['signup_password'];
		$email = $user['signup_email'];
		$usertype = $user['signup_usertype'];
		$firstname = $user['signup_firstname'];
		$lastname = $user['signup_lastname'];
		
		// Check for password length requirement
		if (strlen($password) < 4)
			return 2;

		// Password is ok, so hash and salt it
		include_once('model/PasswordHash.php');
		$hasher = new PasswordHash(8, FALSE);
		$hashedPassword = $hasher->HashPassword($password);

		// Make sure this username isn't already taken
		include_once('model/dbfun.php');
		$db = makeDBConnection();
		$sql = 'SELECT username FROM users WHERE username = ' . dbSafe($db, $username) . ';';
		$result = mysqli_query($db, $sql);
		$avail = TRUE;
		while ($row = mysqli_fetch_array($result)) {
			if (strtoupper($row['username']) == strtoupper($username)) {
				mysqli_close($db);
				return 3;
			}
		}
		
		// Write user info to database
		$sql = 'INSERT INTO users 
				(username, passwd, email, joined, category, firstname, lastname, state, zip)
				VALUES 
				('.dbSafe($db, $username).', '.dbSafe($db, $hashedPassword).', '
				.dbSafe($db, $email).', '.dbSafe($db, date('Y-m-d H:i:s')).', '
				.intval($usertype).', '.dbSafe($db, $firstname).', '
				.dbSafe($db, $lastname).', '.dbSafe($db, $state).', '
				.dbSafe($db, $zip).');';
		if (!mysqli_query($db, $sql)) {
			mysqli_close($db);
			return 4;
		}
		$_SESSION['loggedin'] = TRUE;
		$_SESSION['username'] = $username;
		$_SESSION['usertype'] = intval($usertype);
		mysqli_close($db);
		return 0;
	}

	public function login($username, $password) {
		/*
		Return values:
		0 = success
		1 = bad username
		2 = bad password
		*/ 
		// Get user info from DB
		include_once('model/dbfun.php');
		$db = makeDBConnection();
		$query = 'SELECT * FROM users WHERE username = '.dbSafe($db, $username).';';
		$result = mysqli_fetch_array(mysqli_query($db, $query));
		$stored_hashpass = $result['passwd'];
		mysqli_close($db);
		
		// Make sure the username exists
		if (!$result) 
			return 1;
			
		// If it does, check the password and login
		include_once('model/PasswordHash.php');
		$hasher = new PasswordHash(8, FALSE);
		if ($hasher->CheckPassword($password, $stored_hashpass)) {
			$_SESSION['loggedin'] = TRUE;
			$_SESSION['username'] = $username;
			return 0;
		}
		
		// Otherwise, exit with error
		return 2;
	}
	
	public function logout() {
		$_SESSION['loggedin'] = FALSE;
		unset($_SESSION['username']);
	}
	
	/**
	 * Fetch information needed to generate sickness map.
	 */
	public function sick_map() {
		include_once('model/dbfun.php');
		include_once('model/datetime.php');
		$db = makeDBConnection();
		$sick_map = $this->get_sick_counts($db);
		$updated = $this->get_updated($db);
		mysqli_close($db);
		return array($sick_map, $updated);
	}
		
	/**
	 * Get count data most recently written to database.
	 */
	protected function get_updated($db) {
		$sql = 'SELECT MAX(written) FROM state_sick_counts;';
		$result = mysqli_fetch_array(mysqli_query($db, $sql));
		$updated = array();
		$updated = processDateTime($result[0]);
		return $updated;
	}
	
	/**
	 * Get sick-word-to-place-name associations from database.
	 */
	protected function get_sick_counts($db) {
		$sql = '
			SELECT ssc0.state_id, s.name, s.latitude, s.longitude, ssc0.sick_words, s.pop_2010
			FROM 
			(
				SELECT s1.*, p.pop_2010 FROM populations p
				INNER JOIN
				states s1 ON p.name = s1.name
			) s
			RIGHT JOIN
			(
				SELECT ssc.state_id, ssc.sick_words, smax.written 
				FROM state_sick_counts ssc
				INNER JOIN
				(
					SELECT state_id, MAX(written) AS written 
					FROM state_sick_counts GROUP BY state_id
				) smax
				ON ssc.written = smax.written
				WHERE ssc.state_id = smax.state_id
			) ssc0
			ON ssc0.state_id = s.id
			WHERE ssc0.sick_words > 0
			AND s.name IS NOT NULL
			AND ssc0.written > DATE_SUB(NOW(), INTERVAL 30 DAY);
		';
		$result = mysqli_query($db, $sql);
		$sick_map = array();
		while ($row = mysqli_fetch_array($result))
			$sick_map[] = $row;
		return $sick_map;
	}
	
}
