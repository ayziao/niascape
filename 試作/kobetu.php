<?php 
header('Content-Type: text/html; charset=UTF-8');
//個別ページ

$ini_array = parse_ini_file("setting.ini");
$location  = $ini_array['sqlite_file'];
$handle    = new SQLite3($location); 

//$site = $_GET["site"] ? $_GET["site"] : $ini_array['default_site'];
$path = array_pop(explode('/', substr($_SERVER["SCRIPT_NAME"],1)));	//リクエスト末尾から/の直後までを取得 ルーティングで末尾数字20文字判定済み前提

//PENDING サイト判定いれるか
$query = <<< EOM

SELECT * 
FROM basedata 
WHERE  identifier = '$path'

EOM;
//AND site = '$site' 

$results = $handle->query($query); 
$raw = $results->fetchArray();

if ($raw) {
	print('<pre>');
	var_dump($query);
	var_dump($raw);
	var_dump($_SERVER['HTTP_HOST']);
	var_dump(explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0]);
	var_dump($_SERVER);


	// print('</pre>');
} else {
	return false;
}


//TODO HTML組み立て

