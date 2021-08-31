<?php
require_once "./functions.php";

use DigitalStars\SimpleAPI;

// localhost testing header
header("Access-Control-Allow-Origin: *");

$api = new SimpleAPI();

switch ($api->module) {
	// Test requests
	case "get_success":
		$data = $api->params([]);

		$api->answer["status"] = true;
		$api->answer["response"] = ["payload" => "success", "input_headers" => getallheaders(), "output_headers" => apache_response_headers()];
		break;

	case "get_error":
		$data = $api->params([]);

		$api->answer["status"] = false;
		$api->answer["reason"] = "Example of error message";
		break;
}