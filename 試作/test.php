<?php 
date_default_timezone_set('Asia/Tokyo');
//phpinfo();

// \r\n検索

$ini_array = loadIni();
$handle = new SQLite3($ini_array['sqlite_file2']); 

$search = "\r\n";

$query = <<< EOM
SELECT * FROM basedata
WHERE body LIKE '%$search%' 
ORDER BY identifier ASC LIMIT 1000
EOM;
var_dump($query);

$results = $handle->query($query); 

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	var_dump($row);
}

$query = <<< EOM
SELECT count(*) FROM basedata
WHERE body LIKE '%$search%' 
EOM;
var_dump($query);

$results = $handle->query($query); 
while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	var_dump($row);
}


$query = <<< EOM
SELECT count(*) FROM basedata
EOM;
var_dump($query);

$results = $handle->query($query); 
while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	var_dump($row);
}
