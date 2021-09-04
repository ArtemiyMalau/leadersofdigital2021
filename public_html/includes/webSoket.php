<?php

require_once __DIR__ . '/vendor/autoload.php';

require_once __DIR__ . "/functions.php";

use Workerman\Lib\Timer;
use Workerman\Worker;


$connections = []; // сюда будем складывать все подключения

// Стартуем WebSocket-сервер на порту 27800
$worker = new Worker("websocket://0.0.0.0:2346");

function getDataUser()
{
    global $db;
//    if (isset($_COOKIE["token"])) {
        try {
            $token = $_COOKIE["token"];
            //$userData = $db->query("SELECT * FROM `user` WHERE `token` = ?s", [$token])->fetch();
            $userData = $db->query("SELECT * FROM `user` WHERE `id` = ?i", [92])->fetch();
            echo implode(" ", $userData);
            if ($userData) {
                return ["status" => true, "user_data" => $userData];
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
//    } else {
//        return ["status" => false, "reason" => "NO_TOKEN"];
//    }
}

function getUserDialogsView($id) //для левой панели выбора диалогов
{
    global $db;

    $response = [];
    $res = $db->query("SELECT `dialog_id` FROM `chat_dialog` WHERE `dialog_one_user_id` = ?i OR `dialog_two_user_id` = ?i ", [$id, $id])->fetchAll();
    foreach ($res as $dialogId) {
        $lastMessage = $db->query("SELECT `text` FROM `chat_message` WHERE `fk_dialog_id` = ?i ORDER BY `time` DESC", [$dialogId["dialog_id"]])->fetch();
        $response[] = [
            "dialog_id" => $dialogId,
            "last_message" => $lastMessage["text"]
        ];
    }
    return $response;
}

$worker->onWorkerStart = function ($worker) use (&$connections) {
    $interval = 5; // пингуем каждые 5 секунд
    Timer::add($interval, function () use (&$connections) {
        foreach ($connections as $c) {
            // Если ответ не пришел 5 раза, то удаляем соединение из списка
            // и оповещаем всех участников об "отвалившемся" пользователе
            if ($c->pingWithoutResponseCount >= 5) {
                unset($connections[$c->id]);

                $messageData = [
                    "action" => "Offline",
                    "userId" => $c->id,
                ];
                $message = json_encode($messageData);

                $c->destroy(); // уничтожаем соединение

                foreach ($connections as $connection) {
                    $connection->send($message);
                }
            } else {
                $c->send('{"action":"Ping"}');
                $c->pingWithoutResponseCount++; // увеличиваем счетчик пингов
            }
        }
    });
};

$worker->onConnect = function ($connection) use (&$connections) {
    $connection->onWebSocketConnect = function ($connection) use (&$connections) {
        $res = getDataUser();
        echo "123";

        $connection->send(json_encode($res));

        if ($res["status"] == true) {
            echo "qq";
            $userData = $res["user_data"];

            $connection->userId = $userData["id"];
            $connection->pingWithoutResponseCount = 0;

            $userDialogView = getUserDialogsView($connection->userId);

            $connectionMessageDate = [
                "action" => "Connection",
                "user_id" => $connection->userId,
                "user_dialog_view" => $userDialogView
            ];
            $connection->send(json_encode($connectionMessageDate));

            $usersMessageData = [
                "action" => "Online",
                "user_id" => $connection->userId,
            ];

            foreach ($connections as $c) {
                if ($c->userId != $userData["id"]) {
                    $c->send(json_encode($usersMessageData));
                }
            }
        }
    };
};

$worker->onClose = function ($connection) use (&$connections) {
    // Эта функция выполняется при закрытии соединения
    if (!isset($connections[$connection->id])) {
        return;
    }

    // Удаляем соединение из списка
    unset($connections[$connection->id]);

    // Оповещаем всех пользователей о выходе участника из чата
    $messageData = [
        "action" => "Offline",
        'userId' => $connection->id
    ];
    $message = json_encode($messageData);

    foreach ($connections as $c) {
        $c->send($message);
    }
};

$worker->onMessage = function ($connection, $message) use (&$connections) {
    global $db;
    $messageData = json_decode($message, true);
    $toUserId = isset($messageData['to_user_id']) ? (int)$messageData['to_user_id'] : 0;
    $action = isset($messageData['action']) ? $messageData['action'] : '';
    $dialogId = isset($messageData["dialog_id"]) ? $messageData["dialog_id"] : -1;
    if ($action == 'Pong') {
        // При получении сообщения "Pong", обнуляем счетчик пингов
        $connection->pingWithoutResponseCount = 0;
    } else {
        $messageData['action'] = 'Message';

        $messageData["time"] = time();
        // Дополняем сообщение данными об отправителе
        $messageData['userId'] = $connection->id;
        // Преобразуем специальные символы в HTML-сущности в тексте сообщения
        // Заменяем текст заключенный в фигурные скобки на жирный
        $messageData['text'] = preg_replace('/\{(.*)\}/u', '<b>\\1</b>', htmlspecialchars($messageData['text']));

        $db->query("INSERT INTO `chat_message`(`text`, `fk_dialog_id`, `fk_user_id`, `fk_to_user_id`, `isRead`, `isVisible`, `time`) VALUES ( ?s, ?i, ?i, ?i, 1, 1, ?i)",
            [$messageData['text'], $dialogId, $messageData['userId'], $toUserId, $messageData["time"]]);

        if (isset($connections[$toUserId])) {
            // Отправляем приватное сообщение указанному пользователю
            $connections[$toUserId]->send(json_encode($messageData));
            // и отправителю
            $connections->send(json_encode($messageData));
        } else {

            $connection->send(json_encode($messageData));
        }

    }
};


Worker::runAll();