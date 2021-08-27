<?php
require_once "./functions.php";

use DigitalStars\SimpleAPI;

$api = new SimpleAPI();

switch ($api->module) {
	// Test requests
	case "get_success":
		$data = $api->params([]);

		$api->answer["status"] = true;
		$api->answer["response"] = ["payload" => "success"];
		break;

	case "get_error":
		$data = $api->params([]);

		$api->answer["status"] = false;
		$api->answer["error"] = "Example of error message";
		break;
}