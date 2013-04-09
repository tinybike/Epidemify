<?php
include_once('model/Model.php');

class Controller {
	private $model;
	private $page;
	
	public function __construct() {
		$this->model = new Model();
		$this->page = (isset($_GET['page'])) ? $_GET['page'] : 'default';
	}
	
	public function invoke() {
		switch ($this->page) {
			// Create new account
			case 'signup':
				$signup = $this->model->signup($_POST);
			
			// Login to an existing account
			case 'login':
				$login = $this->model->login($_POST['login_username'], $_POST['login_password']);
				
			// Logout
			case 'logout':
				$this->model->logout();
	
			// By default, show the splash screen
			default:
				list($sick_map, $updated) = $this->model->sick_map();
				include 'view/splash.php';
				break;
		}
	}
}
