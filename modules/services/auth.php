<?php
	error_reporting(false);
	
	$auth = file_get_contents('auth.txt');
	$auth = explode(',', $auth);
	mysql_connect('localhost', trim($auth[0]), trim($auth[1]));
	
	if(mysql_connect('localhost',  trim($auth[0]),  trim($auth[1]))){
		echo "success\n";
	}else{
		echo "failure\n";
	}
?>