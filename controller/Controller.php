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
				include 'view/splash.php';
				break;
			
			// Login to an existing account
			case 'login':
				$login = $this->model->login($_POST['login_username'], $_POST['login_password']);
				include 'view/splash.php';
				break;
				
			// Logout
			case 'logout':
				$this->model->logout();
				include 'view/splash.php';
				break;	

			// Social network
			case 'network':			
				$subpage = (isset($_GET['sub'])) ? $_GET['sub'] : 'default';
				switch ($subpage) {
					// Search for new friends
					case 'search':
						$findlinks = $this->model->findlinks($_POST['findlinks']);
						include 'view/findlinks.php';
						break;
					// Make new friend
					case 'add':
						$addlink = $this->model->addlink($_SESSION['username'], $_POST['addlink']);
						include 'view/addlink.php';
						break;
					// Fetch list of friends
					default:
						$links = $this->model->getlinks();
						include 'view/network.php';
				}
				break;
			
			// Edit your profile
			case 'profile':
				if ($_POST['update_profile']) {
					$update_profile = $this->model->update_profile();
					include 'view/update_profile.php';
				}
				else {
					$profile = $this->model->profile();
					include 'view/profile.php';
				}
				break;
	
			// By default, show the splash screen
			default:
				$sick_map = $this->model->sick_map();
				include 'view/splash.php';
				break;
		}
	}
}
