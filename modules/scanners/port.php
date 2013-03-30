<?php
error_reporting(0);
$host = $argv[1];
$range = explode('-', $argv[2]);
for($i=$range[0]; $i<=$range[1]; $i++){
    $f = fsockopen($host, $i);
    if($f){
        echo "Connection to " . $host . " port " . $i . " succeeded!\n";
    }
    fclose($f);
}
?>
