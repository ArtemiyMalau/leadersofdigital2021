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
        $api->answer = $res;
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

        $okveds = $db->query("SELECT `level` , `name` FROM `okved_2` ORDER BY okved_2.code ASC")->fetchAll();
        $api->answer = [
            "status" => true,
            "response" => [
                "okveds" => $okveds
            ],
        ];
        break;

    case "okved_search":
        $data = $api->params(["?okveds_names", "?page", "?cities", "?query"]);
        if (!isset($data["page"])) {
            $data["page"] = 1;
        }
        $isWhere = 0;
        $selectPage = (int)$data["page"];
        $sql = "SELECT vr.id, vr.ogrn, vr.inn, vr.kpp, vr.name, vr.address, vr.email, vr.website, vr.phone, IFNULL(vr.rate_backend , 10) AS rate_minpromtorg FROM vendor vr JOIN okved_2_vendor ok_vr ON vr.id = ok_vr.vendor_id";
        if (isset($data["okveds_names"])) {
            $okvedNames = $data["okveds_names"];
            if (count($okvedNames) != 0) {
                $isWhere = 1;
                $sql .= " WHERE ";
                $okvedsIds = [];
                foreach ($okvedNames as $okvedname) {
                    $okvedsId = $db->query("SELECT id FROM okved_2 WHERE `name` LIKE ?s", [$okvedname])->fetch();
                    $okvedsIds[] = $okvedsId["id"];
                }
                foreach ($okvedsIds as $okvedsId) {
                    $sql .= "ok_vr.okved_id = " . $okvedsId;
                    $sql .= " OR ";
                }
                $sql = substr($sql, 0, -3);
            }
        }
        if (isset($data["cities"])) {
            $cities = $data["cities"];
            if (count($cities) != 0) {
                if ($isWhere) {
                    $sql .= " AND ";
                } else {
                    $isWhere = 1;
                    $sql .= " WHERE ";
                }
                foreach ($cities as $city) {
                    $city = mb_strtoupper($city);
                    $sql .= "vr.address LIKE '%{$city}%'";
                    $sql .= " OR ";
                }
                $sql = substr($sql, 0, -3);
            }
        }
        if (isset($data["query"])) {
            $query = $data["query"];
            if ($isWhere) {
                $sql .= " AND ";
            } else {
                $isWhere = 1;
                $sql .= " WHERE ";
            }
            $sql .= "vr.name LIKE '%{$query}%'";
        }
        $sql .= " GROUP BY vr.id ORDER BY vr.rate_backend DESC, vr.rate_minpromtorg DESC, vr.rate_client DESC";

        $limit = 10;
        $offset = 0 + 10 * ($selectPage - 1);
        $page = " LIMIT {$limit} OFFSET {$offset}";
        $countPage = count($db->query($sql)->fetchAll());
        $countPage = ceil($countPage / 10);
        $sql .= $page;
        //result request
        $vendorsItems = $db->query($sql)->fetchAll();
        $api->answer = [
            "status" => true,
            "response" => [
                "count_items" => count($vendorsItems),
                "items" => $vendorsItems,
                "count_page" => $countPage,
                "current_page" => (int)$selectPage
            ],
        ];
        break;

    case "get_user_data":
        $data = $api->params([]);
        $res = getUserData();
        $api->answer = $res;
        break;

    case "change_user_data":
        $data = $api->params(["user_type", "email", "phone", "old_password", "new_password", "name", "optional_name"]);
        $res = changeUserData($data["user_type"], $data["email"], $data["phone"], $data["old_password"], $data["new_password"], $data["name"], $data["optional_name"]);
        $api->answer = $res;
        break;

    case "get_all_cities":
        $data = $api->params([]);
        $allCity = $db->query("SELECT name FROM city ORDER BY id ASC")->fetchAll();
        $res = [];
        foreach ($allCity as $city) {
            $res[] = $city["name"];
        }
        $api->answer = $res;

        break;

    case "send_vendor_mail":
        $data = $api->params(["vendor_id"]);
        $res = sendMailRequest($data["vendor_id"]);
        $api->answer = $res;
        break;

    case "get_mailes_send":
        $data = $api->params([]);
        $res = getAllMessageSend();
        $api->answer = $res;
        break;


    case "add_to_favorites":
        $data = $api->params(["vendor_id"]);
        $res = addToFavorites($data["vendor_id"]);
        $api->answer = $res;
        break;

    case "get_all_favorites":
        $data = $api->params([]);
        $res = getAllFavorites();
        $api->answer = $res;
        break;
}