<?php
/*
 * 検索
 */
header('Content-Type: text/html; charset=UTF-8');

$ini_array = parse_ini_file(dirname(__FILE__) . "/setting.ini");

if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
	$site = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0];
} else {
	$site = explode("/", substr($_SERVER["SCRIPT_NAME"], 2))[0];
}

$searchbody = $_GET['searchbody'];
$order = isset($_GET['order']) ? $_GET['order'] : 'DESC';

$command = "python3 /Volumes/data/niascape/niascape searchbody";
$command .= $site ? ' --site=' . escapeshellarg($site) : '';
$command .= $searchbody ? ' --searchbody=' . escapeshellarg($searchbody) : '';
$command .= $order ? ' --order=' . escapeshellarg($order) : '';
exec($command, $out, $ret);
$timeline = json_decode(end($out), true);

$day = '';
$order = ($order == 'DESC') ? 'ASC' : 'DESC';

foreach ($timeline as $row) {
	//TODO 時間区切りを入れる
	$day2 = substr($row['datetime'], 0, 10);
	if ($day != $day2) {
		$content .= ($day != '') ? '</div>' : '';
		$content .= '<h5><a href="./' . str_replace('-', '', $day2) . '">' . $day2 . '</a></h5><div class="lines">';
		$day = $day2;
	}

	$tagstr = '';
	$tags = explode(' ', trim($row['tags']));
	foreach ($tags as $value) {
		if (strpos($value, '#') === 0) {
			$tag = substr($value, 1);
			$tagstr .= ' <a href="./?tag=' . $tag . '">' . $tag . '</a>';
		}
	}

	$content .= '<div class="line"><span class="time"><a href="./' . $row['identifier'] . '">' . substr($row['datetime'], 11, 10) . '</a></span>&thinsp;' . $row['body'] . $tagstr . '</div>' . "\n";
}
$content .= '</div>';
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title><?= $searchbody ?> <?= $site ?></title>
		<link rel="icon" type="image/png" href="./favicon.png">
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="./css.css">
	</head>

	<body>
		<h1><a href="./"><?= $site ?></a> <?= $searchbody ?></h1>
		<div id="etc"></div>

		<div class="navi">
			<a href="./?searchbody=<?= $searchbody ?>&order=<?= $order ?>"><?= $order ?></a>
		</div>

		<div>
			<?= $content ?>
		</div>

		<div><a href="./">top</a></div>
		<form action="./" method="GET">
			<input id="search" class="text" type="text" name="searchbody">
			<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
		</form>
	</body>
</html>
