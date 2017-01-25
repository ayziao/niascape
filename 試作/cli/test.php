<?php
/*
 * ツイッタータイムラインストリーム保存したやつ読む
 */

date_default_timezone_set('Asia/Tokyo');
// phpinfo();
//require('common.php');
var_dump($argv);

$file = fopen($argv[1], "r");
if (!$file) {
	fclose($file);
	exit();
}

$count = ['friends' => 0, 'tw' => 0, 'rt' => 0, 'delete' => 0, 'scrub_geo' => 0, 'favrare' => 0, 'favri' => 0, 'event' => '■■■■■■■■■■■■■■'];
$progress = 0;
$favrare = [];
$favri = [];
$user = [];

$ini_array = parse_ini_file(dirname(__FILE__) . "/setting.ini");
$location = $ini_array['twitterdb'];
$handle = new SQLite3($location);

while ($line = fgets($file)) {
	$twit = json_decode($line, true);
	if ($twit['friends']) {
		$count['friends'] ++;
	} elseif ($twit['retweeted_status']) {
		$count['rt'] ++;
	} elseif ($twit['text']) {
		if ($count['tw'] == 0) {
			var_dump($twit);
		}
		$count['tw'] ++;
		$user[$twit['user']['id']] = $twit['user'];
	} elseif ($twit['delete']) {
		$count['delete'] ++;
	} elseif ($twit['scrub_geo']) {
		$count['scrub_geo'] ++;
	} elseif ($twit['event']) {
		$count[$twit['event']] ++;
		if ($twit['event'] == 'favorite') {
			if ($twit['source']['screen_name'] == $argv[3]) {
				$favri[$twit['target']['screen_name']] ++;
				$count['favri'] ++;
				$favraretotalcount += $value;
			} else {
				// if(!$fav[$twit['source']['id']]){
				// 	$fav[$twit['source']['id']] = ['name' => $twit['source']['screen_name'], 'count' => 0];
				// }
				// $fav[$twit['source']['id']]['count']++;
				$favrare[$twit['source']['screen_name']] ++;
				$count['favrare'] ++;
			}
		} elseif ($twit['event'] == 'favorited_retweet') {
			//var_dump($twit);
		}
		// if($count['favorite'] == 1){
		// 	var_dump($twit);
		// }
	} else {
		//var_dump($twit);
	}
	$progress ++;
	if ($progress > 1000) {
		echo ".";
		$progress = 0;
	}
}
fclose($file);

echo "\n";
var_dump($count);
asort($favrare);
asort($favri);
//var_dump($fav);

foreach ($favrare as $key => $value) {
	$favrarelink .= '<a href="https://twitter.com/' . $key . '">' . "$key</a> ($value)<br>\n";
	$favraretotalcount += $value;
}

foreach ($favri as $key => $value) {
	$favrilink .= '<a href="https://twitter.com/' . $key . '">' . "$key</a> ($value)<br>\n";
	$favritotalcount += $value;
}

ob_start();
?>
<html>
	<head>
		<title>ふぁぼ</title>
	</head>
	<body>
		<h1><?= $argv[1] ?></h1>
		<h2>ふぁられ <?= $count['favrare'] ?></h2>
		<?= $favrarelink ?>
		<h2>ふぁぼり <?= $count['favri'] ?></h2>
		<?= $favrilink ?>
	</body>
</html>
<?php
$dump = ob_get_contents();
ob_end_clean();

file_put_contents($argv[2] . '/fav.html', $dump);

$query = 'INSERT OR REPLACE INTO user VALUES ';
foreach ($user as $key => $value) {
//	dbreplace($handle, $key, $value['screen_name']);
	$query .= "($key,'" . $value['screen_name'] . "'),";
}

$query = substr($query, 0, -1);
//var_dump($query);

$handle->query($query);
