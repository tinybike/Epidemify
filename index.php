<?php
session_start();
include_once('setpath.php');
include_once('controller/Controller.php');
$controller = new Controller();
$controller->invoke();
