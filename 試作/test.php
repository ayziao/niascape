<?php

//ツイッタータイムラインストリーム保存したやつ読む

date_default_timezone_set('Asia/Tokyo');
// phpinfo();
//require('common.php');
var_dump($argv);

$file = fopen($argv[1], "r");
if (!$file) {
	fclose($file);
	exit();
}

$count = ['friends' => 0, 'tw' => 0, 'rt' => 0, 'delete' => 0, 'scrub_geo' => 0, 'event' => '■■■■■■■■■■■■■■'];
$count2 = 0;

while ($line = fgets($file)) {
	$aaa = json_decode($line, true);
	if ($aaa['friends']) {
		$count['friends'] ++;
	} elseif ($aaa['retweeted_status']) {
		$count['rt'] ++;
	} elseif ($aaa['text']) {
		$count['tw'] ++;
	} elseif ($aaa['delete']) {
		$count['delete'] ++;
	} elseif ($aaa['scrub_geo']) {
		$count['scrub_geo'] ++;
	} elseif ($aaa['event']) {
		$count[$aaa['event']] ++;
	} else {
		var_dump($aaa);
	}
	$count2++;
	if ($count2 > 1000) {
		echo ".";
		$count2 = 0;
	}
}
fclose($file);

echo "\n";
var_dump($count);

