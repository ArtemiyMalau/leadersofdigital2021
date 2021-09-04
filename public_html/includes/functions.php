<?php

require_once __DIR__ . "/vendor/autoload.php";
require_once __DIR__ . "/config.php";

use DigitalStars\DataBase\DB;
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

const JSON_OPTIONS = JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_NUMERIC_CHECK | JSON_PRESERVE_ZERO_FRACTION;

$db = new DB("{$config["db"]["type"]}:host={$config["db"]["host"]};dbname={$config["db"]["database"]}",
    $config["db"]["user"],
    $config["db"]["password"],
    [
        PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES 'utf8'",
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);

if (!$db) {
    echo "Connection false";
    exit();
}

// сообщения по почте
$mail = new PHPMailer(true);
$mail->isSMTP();
$mail->Host = 'ssl://smtp.yandex.ru';
$mail->SMTPAuth = true;
$mail->Username = 'egor.salnik0v';
$mail->Password = 'K4M24UCmZlWi';
$mail->Port = 465;

function sign($user)
{
    global $db;
    $token = setToken();
    $db->query("UPDATE `user` SET `token` = ?S where `id` = ?s ", [$token, $user['id']]);
    return ["status" => true];
}

function signIn($login, $pass)
{
    $user = getUser($login, $pass);
    if ($user) {
        return sign($user);
    } else {
        return ["status" => false];
    }
}

function getUser($email, $password)
{
    global $db;
    $rnd = $db->query("SELECT `rnd` FROM `user` WHERE `login` = ?s", [$email])->fetch();
    $saltedPassword = md5($password . $rnd['rnd']);
    return $db->query("SELECT * FROM `user` WHERE `login` = ?s AND `password` = ?s", [$email, $saltedPassword])->fetch();
}

function signUpCustomer($firstName, $lastName, $email, $password, $phone)
{
    $res = addCustomer($firstName, $lastName, $email, $password, $phone);
    if ($res["status"] == true) {
        $status = sendRegMail($email, $res["token"]);
        $res["mail_send"] = $status;
    }
    return $res;
}

function addCustomer($firstName, $lastName, $email, $password, $phone)
{
    global $db;
    try {
        $db->query("START TRANSACTION;");
        $is_login = $db->query("SELECT * FROM `user` WHERE `login` = ?s", [$email])->fetch();
        if ($is_login) {
            return ["status" => false, "reason" => "THIS LOGIN ALREADY USES"];
        }
        $salt = generateSalt();
        $saltedPassword = md5($password . $salt);
        $token = setToken();
        $db->query("INSERT INTO `user` (`login`, `password`, `rnd`, `token`, `type`) VALUES (?s,?s, ?s, ?s, ?i) ", [$email, $saltedPassword, $salt, $token, 1])->fetch();
        $res = $db->query("SELECT `id` FROM `user` WHERE `login` = ?s", [$email])->fetch();
        //
        // 1 - заказчик
        // 2 - поставщик
        //
        $db->query("INSERT INTO `customer_data` (`user_id`, `first_name`, `last_name`, `phone`, `email` ) VALUES (?i,?s, ?s, ?s, ?s)", [$res['id'], $firstName, $lastName, $phone, $email]);
        $token = generateToken();
        $db->query("INSERT INTO `reg_tokens` SET `user_id` = ?i , `token` = ?s;", [$res['id'], $token]);
        $db->query("COMMIT;");
        return ["status" => true, "token" => $token];
    } catch (Exception $ex) {
        $db->query("ROLLBACK;");
        return ["status" => false, "reason" => $ex->getMessage(), "notify_msg" => "Ошибка при регистрации"];
    }
}

function signUpVendor($companyName, $description, $email, $password)
{
    return addVendor($companyName, $description, $email, $password);
}

function addVendor($companyName, $description, $email, $password)
{
    global $db;
    try {
        $db->query("START TRANSACTION;");
        $is_login = $db->query("SELECT * FROM `user` WHERE `login` = ?s", [$email])->fetch();
        if ($is_login) {
            return ["status" => false, "reason" => "THIS LOGIN ALREADY USES"];
        }
        $salt = generateSalt();
        $saltedPassword = md5($password . $salt);
        $token = setToken();
        $db->query("INSERT INTO `user` (`login`, `password`, `rnd`, `token`, `type`) VALUES (?s,?s, ?s, ?s, ?i) ", [$email, $saltedPassword, $salt, $token, 2])->fetch();
        $res = $db->query("SELECT `id` FROM `user` WHERE `login` = ?s", [$email])->fetch();

        $vendor = $db->query("SELECT * FROM `vendor` WHERE `name` = ?s", [$companyName])->fetch();
        if ($vendor == false) {
            $vendor["id"] = null;
        }

        $db->query("INSERT INTO `vendor_data` (`user_id`, `vendor_id`, `company_name`, `description` ) VALUES (?i, ?i, ?s, ?s)",
            [$res['id'], $vendor["id"], $companyName, $description]);
        $token = generateToken();
        $db->query("INSERT INTO `reg_tokens` SET `user_id` = ?i, `token` = ?s;", [$res['id'], $token]);
        $db->query("COMMIT;");
        return ["status" => true, "token" => $token];
    } catch (Exception $ex) {
        $db->query("ROLLBACK;");
        return ["status" => false, "reason" => $ex->getMessage(), "notify_msg" => "Ошибка при регистрации"];
    }
}

function setToken()
{
    $token = generateToken();
    setcookie("token", $token, time() + 604800, '/');
    return $token;
}

function generateToken()
{
    $token = sprintf(
        '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
        mt_rand(0, 0xffff),
        mt_rand(0, 0xffff),
        mt_rand(0, 0xffff),
        mt_rand(0, 0x0fff) | 0x4000,
        mt_rand(0, 0x3fff) | 0x8000,
        mt_rand(0, 0xffff),
        mt_rand(0, 0xffff),
        mt_rand(0, 0xffff)
    );

    return $token;
}

function generateSalt()
{
    $salt = '';
    $saltLength = 8;
    for ($i = 0; $i < $saltLength; $i++) {
        $salt .= chr(mt_rand(33, 126));
    }
    return $salt;
}

function checkAuth()
{
    global $db;
    if (isset($_COOKIE["token"])) {
        try {
            $token = $_COOKIE["token"];
            $tokenInDb = $db->query("SELECT * FROM `user` WHERE `token` = ?s", [$token])->fetch();
            if ($tokenInDb) {

                return ["status" => true, "token" => $token];
            } else {
                deleteTokenCookie();
                return ["status" => false, "reason" => "INVALID_TOKEN"];
            }
        } catch (SignatureInvalidException $signatureInvalidException) {
            deleteTokenCookie();
            return ["status" => false, "reason" => "SIGNATURE_INVALID_TOKEN"];

        } catch (UnexpectedValueException $ex) {
            deleteTokenCookie();
            return ["status" => false, "reason" => "INVALID_TOKEN"];
        }
    } else {
        return ["status" => false, "reason" => "NO_TOKEN"];
    }
}

function getUserName()
{
    global $db;
    if (isset($_COOKIE["token"])) {
        try {
            $token = $_COOKIE["token"];
            $user = $db->query("SELECT * FROM `user` WHERE `token` = ?s", [$token])->fetch();
            if ($user) {
                if ($user["type"] == 1) {
                    $person = $db->query("SELECT * FROM `customer_data` WHERE `user_id` = ?i", [$user["id"]])->fetch();

                } else if ($user["type"] == 2) {

                }
                return ["status" => true, "first_name" => $person["first_name"], "last_name" => $person["last_name"]];
            } else {
                deleteTokenCookie();
                return ["status" => false, "reason" => "INVALID_TOKEN"];
            }
        } catch (SignatureInvalidException $signatureInvalidException) {
            deleteTokenCookie();
            return ["status" => false, "reason" => "SIGNATURE_INVALID_TOKEN"];

        } catch (UnexpectedValueException $ex) {
            deleteTokenCookie();
            return ["status" => false, "reason" => "INVALID_TOKEN"];
        }
    } else {
        return ["status" => false, "reason" => "NO_TOKEN"];
    }
}

function deleteTokenCookie()
{
    setcookie("token", '', time() - 1000);
    setcookie("token", '', time() - 1000, '/');
}

function verifyAccount($token)
{
    global $db;
    try {
        $db->query("START TRANSACTION;");
        $data = $db->query("SELECT * FROM `reg_tokens` WHERE `token` LIKE ?s and `status` = 0", [$token])->fetch();
        if ($data) {
            $db->query("UPDATE `reg_tokens` SET `status` = 1 WHERE `user_id` = ?i;", [$data['user_id']]);
            $db->query("UPDATE `user` SET `status` = 1 WHERE `id` = ?i;", [$data['user_id']]);
        }
        $db->query("COMMIT;");
    } catch (Exception $ex) {
        $db->query("ROLLBACK;");
    }
}

function sendRegMail($email, $token)
{
    global $mail;
    $mail->setFrom("egor.salnik0v@yandex.ru", 'vibe.digital');
    $mail->isHTML(true);
    $mail->Subject = "RosatomVendors"; // Заголовок письма
    $mail->Body = "Для подтверждения аккаунта перейдите по <a href='https://lagrange.creativityprojectcenter.ru/includes/verify_account.php?token={$token}'>ссылке</a>"; // Текст письма
    $mail->addAddress($email);
    $mail->send();
    try {
        $mailStatus = true;
    } catch (Exception $ex) {
        $mailStatus = false;
    }
    return $mailStatus;
}

function getUserData()
{
    global $db;
    $auth = checkAuth();
    $res = [];
    if ($auth["status"] == true) {
        $userData = $db->query("SELECT * FROM `user` WHERE `token` = ?s", [$auth["token"]])->fetch();
        $response = [
            "email" => $userData["login"],
            "verify_status" => (int)$userData["status"],
        ];
        if ($userData["type"] == 1) {
            $response["user_type"] = 1;
            $customerData = $db->query("SELECT * FROM `customer_data` WHERE `user_id` = ?i", [$userData["id"]])->fetch();
            $response["first_name"] = $customerData["first_name"];
            $response["last_name"] = $customerData["last_name"];
            $response["phone"] = $customerData["phone"];
            $response["avatar"] = $customerData["avatar"];
        } else if ($userData["type"] == 2) {
            $response["user_type"] = 2;
            $vendorData = $db->query("SELECT * FROM `vendor_data` WHERE `user_id` = ?i", [$userData["id"]])->fetch();
            $response["company_name"] = $vendorData["company_name"];
            $response["description"] = $vendorData["description"];
            $response["phone"] = $vendorData["phone"];
            $response["avatar"] = $vendorData["avatar"];
        }
        $res["status"] = true;
        $res["response"] = $response;
    } else {
        $res["status"] = false;
    }
    return $res;
}

function changeUserData($type, $email, $phone, $oldPass, $newPass, $name, $optionalName)
{
    global $db;
    $auth = checkAuth();
    $response = [];
    if ($auth["status"] == true) {
        $userData = $db->query("SELECT * FROM `user` WHERE `token` = ?s", [$auth["token"]])->fetch();
        $oldPass = md5($oldPass . $userData['rnd']);
        if ($oldPass != "" && $newPass != "") {
            if ($oldPass == $userData["password"]) {
                $newPass = md5($newPass . $userData['rnd']);
                $db->query("UPDATE `user` SET `password` = ?S where `id` = ?i", [$newPass, $userData["id"]]);
                $response["password"] = [
                    "change" => true
                ];
            } else {
                $response["password"] = [
                    "change" => false,
                    "reason" => "Старый пароль неверен"
                ];
            }
        }
        if ($email != $userData['login']) {
            $db->query("UPDATE `user` SET `login` = ?S where `id` = ?i", [$email, $userData["id"]]);
            $response["email"] = ["change" => true];
        }
        if ($type == 1) {
            $data = $db->query("SELECT * FROM `customer_data` WHERE `user_id` = ?i", [$userData["id"]])->fetch();
            if ($data["first_name"] != $name) {
                $db->query("UPDATE `customer_data` SET `first_name` = ?S where `id` = ?i", [$name, $userData["id"]]);
                $response["first_name"] = ["change" => true];
            }
            if ($data["last_name"] != $optionalName) {
                $db->query("UPDATE `customer_data` SET `last_name` = ?S where `id` = ?i", [$optionalName, $userData["id"]]);
                $response["last_name"] = ["change" => true];
            }
            if ($data["phone"] != $phone) {
                $db->query("UPDATE `customer_data` SET `phone` = ?S where `id` = ?i", [$phone, $userData["id"]]);
                $response["phone"] = ["change" => true];
            }
        } else if ($type == 2) {
            $data = $db->query("SELECT * FROM `vendor_data` WHERE `user_id` = ?i", [$userData["id"]])->fetch();
            if ($data["company_name"] != $name) {
                $db->query("UPDATE `vendor_data` SET `company_name` = ?S where `id` = ?i", [$name, $userData["id"]]);
                $response["company_name"] = ["change" => true];
            }
            if ($data["description"] != $optionalName) {
                $db->query("UPDATE `vendor_data` SET `description` = ?S where `id` = ?i", [$optionalName, $userData["id"]]);
                $response["description"] = ["change" => true];
            }
            if ($data["phone"] != $phone) {
                $db->query("UPDATE `vendor_data` SET `phone` = ?S where `id` = ?i", [$phone, $userData["id"]]);
                $response["phone"] = ["change" => true];
            }
        }
        return ["status" => false, $response];
    } else {
        return ["status" => false, "reason" => "No_auth"];
    }

}