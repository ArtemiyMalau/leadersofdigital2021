<?php

require_once __DIR__ . "/vendor/autoload.php";

require_once __DIR__ . "/config.php";

use DigitalStars\DataBase\DB;

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