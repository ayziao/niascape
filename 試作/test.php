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
$fav = [];

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
		if($aaa['event'] = 'favorite'){
			// if(!$fav[$aaa['source']['id']]){
			// 	$fav[$aaa['source']['id']] = ['name' => $aaa['source']['screen_name'], 'count' => 0];
			// }
			// $fav[$aaa['source']['id']]['count']++;
			$fav[$aaa['source']['screen_name']]++;
		}
		// if($count['favorite'] == 1){
		// 	var_dump($aaa);
		// }
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
asort($fav);
//var_dump($fav);

foreach ($fav as $key => $value) {
	$bbb .= '<a href="https://twitter.com/'.$key.'">'."$key</a> ($value)<br>\n"; 
}

ob_start();

?>
<html>
	<head>
		<title>ふぁぼられ</title>
	</head>
	<body>
		<h1><?=$argv[1] ?></h1>
		<?=$bbb ?>
	</body>
</html>
<?php

$dump = ob_get_contents();
ob_end_clean();


file_put_contents($argv[2].'/fav.html', $dump);
