<?php
//キュー

date_default_timezone_set('Asia/Tokyo');
$ini_array = parse_ini_file(dirname(__FILE__) . "/../setting.ini");
$handle = new SQLite3($ini_array['sqlite_file']);

$datetime = date('Y-m-d H:i:s');

$query = <<< EOM

SELECT * 
FROM queue 
WHERE  reservation_time < '$datetime'
ORDER BY reservation_time , serial_number ASC

EOM;

// WHERE  identifier = '$id'

//AND site = '$site'  //PENDING サイト判定いれるか
//var_dump($query);
$results = $handle->query($query);
$raw = $results->fetchArray(SQLITE3_ASSOC);

if($raw['queue_type'] == 'shell_command'){
	echo $raw['content'],"\n";
	exec($raw['content']);
	
	$num = $raw['serial_number'];
$query = <<< EOM

DELETE FROM	queue
WHERE	serial_number = $num

EOM;

	var_dump($query);
	$re = $handle->query($query);
//	var_dump($re);
}

//echo "kyu- \n";
var_dump($raw);


