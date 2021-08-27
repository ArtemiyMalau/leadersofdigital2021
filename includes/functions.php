<?php

require_once __DIR__ . "/vendor/autoload.php";

require_once __DIR__ . "/config.php";

use Krugozor\Database\Mysql;

const JSON_OPTIONS = JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_NUMERIC_CHECK | JSON_PRESERVE_ZERO_FRACTION;

$db = Mysql::create($config["db"]["host"], $config["db"]["user"], $config["db"]["password"])
	->setDatabaseName($config["db"]["database"])->setCharset("utf8");
if (!$db) {
	echo "Connection false";
	exit();
}