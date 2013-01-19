<?php
	error_reporting(false);
	
	$auth = file_get_contents('auth.txt');
	$auth = explode(',', $auth);
	
	if(mysql_connect(trim($auth[2]),  trim($auth[0]),  trim($auth[1]))){
		echo "success\n";
	}else{
		echo "failure\n";
	}
?>
