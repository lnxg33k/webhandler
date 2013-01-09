<?php

$auth = file_get_contents('auth.txt');
$auth = explode(',', $auth);
mysql_connect('localhost', trim($auth[0]), trim($auth[1]));
$query = file_get_contents('sql.txt');
$queies = explode(";", $query);
foreach ($queies as $query) {
	if (trim($query) != "") {
		$result = @mysql_query($query);
		if (!$result) {
			echo mysql_error();
		}
	}
}
$rows = array();
while ($row = mysql_fetch_assoc($result)) {
	$rows[] = $row;
}
print json_encode($rows);
echo "\n";
?>
