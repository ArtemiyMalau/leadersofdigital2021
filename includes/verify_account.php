<?php

require_once __DIR__ . "/vendor/autoload.php";
require_once __DIR__ . "/functions.php";

if (isset($_GET['token'])){
    $token =  $_GET['token'];
    $res = verifyAccount($token);
    header('Location: http://lagrange.creativityprojectcenter.ru/', true);
}
