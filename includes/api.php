<?php
require_once "./functions.php";

use DigitalStars\SimpleAPI;

// localhost testing header
// header("Access-Control-Allow-Origin: *");
header('Access-Control-Expose-Headers: Access-Control-Allow-Origin', false);
header('Access-Control-Allow-Origin: *', false);
header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept', false);
header('Access-Control-Allow-Credentials: true');

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

	// Major requests
    case "sign_up_customer":
        $data = $api->params(["first_name", "last_name", "email", "password", "phone"]);
        $res = signUpCustomer($data["first_name"], $data["last_name"], $data["email"], $data["password"], $data["phone"]);
        $api->answer = $res;
        break;

    case "sign_up_vendor":
        $data = $api->params(["company_name", "description", "email", "password"]);
        $res = signUpVendor($data["company_name"], $data["description"], $data["email"], $data["password"]);
        break;

    case "sign_in":
        $data = $api->params(["email", "password"]);
        $res = signIn($data["email"], $data["password"]);
        $api->answer = $res;
        break;

    case "get_user_name":
        $data = $api->params([]);
        $res = getUserName();
        $api->answer = $res;
        break;

    case "check_auth":
        $data = $api->params([]);
        $res = checkAuth();
        $api->answer = $res;
        break;

	case "get_categories":
		$data = $api->params([]);

		$categories = $db->query("SELECT * FROM category ORDER BY category.name ASC")->fetchAll();

		$api->answer = [
			"status" => true, 
			"response" => [
				"categories" => $categories
			],
		];
		break;

	case "get_okved_sections":
		$data = $api->params([]);

		$okved_sections = $db->query("SELECT * FROM okved_section ORDER BY okved_section.code ASC")->fetchAll();

		$api->answer = [
			"status" => true,
			"response" => [
				"okved_sections" => $okved_sections
			],
		];
		break;

	case "get_okveds":
		$data = $api->params([]);

		$okveds = $db->query("SELECT * FROM okved ORDER BY okved.code ASC")->fetchAll();
		$api->answer = [
			"status" => true,
			"response" => [
				"okveds" => $okveds
			],
		];
		break;
}