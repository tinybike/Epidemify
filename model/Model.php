<?php
class Model {

	protected function full_url() {
		$s = empty($_SERVER["HTTPS"]) ? '' : ($_SERVER["HTTPS"] == "on") ? "s" : "";
		$sp = strtolower($_SERVER["SERVER_PROTOCOL"]);
		$protocol = substr($sp, 0, strpos($sp, "/")) . $s;
		return $protocol . "://" . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
	}

	protected function base_url() {
		$actual_link = $this->full_url();
		$exploded_link = explode('?', $actual_link);
		$exploded_link_and = explode('&', $actual_link);
		$base_link = $exploded_link[0];
		return $base_link;
	}

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
		
	// Social net stuff
	public function getlinks() {
		include_once('model/dbfun.php');
		$db = makeDBConnection();
		$query = 'SELECT username, firstname, lastname FROM users WHERE username IN
				  (SELECT user2 FROM friends WHERE user1 = '.dbSafe($db, $_SESSION['username']).'
				  UNION
				  SELECT user1 FROM friends WHERE user2 = '.dbSafe($db, $_SESSION['username']).');';
		$result = mysqli_query($db, $query);
		$links = array();
		while ($row = mysqli_fetch_array($result))
			$links[] = $row;
		mysqli_close($db);
		return $links;
	}
		
	public function findlinks($lookup) {
		include_once('model/dbfun.php');
		$db = makeDBConnection();
		$safe_lookup = dbSafe($db, '%'.$lookup.'%');
		$query = 'SELECT username, firstname, lastname, state, email,
				  CONCAT(CONCAT(firstname, " "), lastname) AS fullname FROM users 
				  HAVING username LIKE '.$safe_lookup.'
				  OR firstname LIKE '.$safe_lookup.'
				  OR lastname LIKE '.$safe_lookup.'
				  OR email LIKE '.$safe_lookup.'
				  OR fullname LIKE '.$safe_lookup.';';
		$result = mysqli_query($db, $query);
		$findlinks = array();
		while ($row = mysqli_fetch_array($result)) {
			if ($_SESSION['username'] != $row['username'])
				$findlinks[] = $row;
		}
		mysqli_close($db);
		return $findlinks;	
	}
	
	public function addlink($linker, $target) {
		// Return values:
		// 0: Error
		// 1: Ok
		// 2: Link already exists
		include_once('model/dbfun.php');
		$db = makeDBConnection();
		$safe_linker = dbSafe($db, $linker);
		$safe_target = dbSafe($db, $target);
		$query = 'SELECT user2 FROM friends WHERE user1 = '.$safe_linker.' AND user2 = '.$safe_target.'
				  UNION
				  SELECT user1 FROM friends WHERE user2 = '.$safe_linker.' AND user1 = '.$safe_target.';';	
		if (mysqli_fetch_array(mysqli_query($db, $query))) {
			mysqli_close($db);
			return 2;
		}
		$query = 'INSERT INTO friends VALUES ('.dbSafe($db, $linker).', '.dbSafe($db, $target).');';
		$result = mysqli_query($db, $query);
		mysqli_close($db);
		return ($result) ? 1 : 0;
	}
		
	public function create_listing($provider, $listing) {
		include_once('model/dbfun.php');
		include_once('model/datetime.php');
		$db = makeDBConnection();
		mysqli_query($db, $query);
		$listing_ID = mysqli_insert_id($db);
		mysqli_close($db);
		return $listing_ID;
	}
}
