<?php
//twitterの全ログファイルからベースデータへ

date_default_timezone_set('Asia/Tokyo');
$ini_array = parse_ini_file(dirname(__FILE__) . "/../setting.ini");
$handle = new SQLite3($ini_array['sqlite_file']);

var_dump($argv);



$dh = opendir($argv[1]);
while (false !== ($filename = readdir($dh))) {
	$files[] = $filename;
}

foreach ($files as $value) {
	if (strpos($value, '.js') > 1) {
		hoge($argv[1] . '/' . $value, $handle ,$argv[2]);
	}
}

function hoge($path, $handle ,$site) {

	$aaa = file_get_contents($path, NULL, NULL, 32);
	$bbb = json_decode($aaa, TRUE);

	$query = 'INSERT INTO basedata (site,identifier,datetime,title,tags,body) VALUES ';
	foreach ($bbb as $value) {
		$timestamp = strtotime($value['created_at']);
		$identifier = date('YmdHis000000', $timestamp);
		$title = $identifier;
		$datetime = date('Y-m-d H:i:s', $timestamp);
		$tags = ' twitter_posted:' . $value['id'];
		foreach ($value['entities']['hashtags'] as $value2) {
			$tags .= ' #' . $value2['text'];
		}
		$tags .= ' ';
		$body =  SQLite3::escapeString($value['text']);
		$query .= "\n('$site','$identifier','$datetime','$title','$tags','$body'),";
	}

	$query = substr($query, 0, -1);

	var_dump($query);
  $result = $handle->query($query);
}
