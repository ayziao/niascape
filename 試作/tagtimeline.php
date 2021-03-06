<?php
/*
 * タグタイムライン
 */
header('Content-Type: text/html; charset=UTF-8');

$ini_array = parse_ini_file(dirname(__FILE__) . "/setting.ini");
if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
	$site = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0];
} else {
	$site = explode("/", substr($_SERVER["SCRIPT_NAME"], 2))[0];
}
$tag = $_GET['tag'];
$order = isset($_GET['order']) ? $_GET['order'] : 'DESC';

$command = "python3 /Volumes/data/niascape/niascape tagtimeline";
$command .= $site ? ' --site=' . escapeshellarg($site) : '';
$command .= $tag ? ' --tag=' . escapeshellarg($tag) : '';
$command .= $order ? ' --order=' . escapeshellarg($order) : '';
exec($command, $out, $ret);
$timeline = json_decode(end($out), true);

$day = '';
$order = ($order == 'DESC') ? 'ASC' : 'DESC';

foreach ($timeline as $row) {
	//TODO 時間区切りを入れる
	$day2 = substr($row['datetime'], 0, 10);
	if ($day != $day2) {
		$content .= ($day != '') ? "\n\t\t\t</div>" : '';
		$content .= "\n\t\t\t" . '<h5><a href="./' . str_replace('-', '', $day2) . '">' . $day2 . '</a></h5> ' . "\n\t\t\t" . '<div class="lines">';
		$day = $day2;
	}
	$tagstr = '';
	$tags = explode(' ', trim($row['tags']));
	foreach ($tags as $value) {
		if (strpos($value, '#') === 0) {
			$taga = substr($value, 1);
			$tagstr .= ' <a href="./?tag=' . $taga . '">' . $taga . '</a>';
		}
	}
	$content .= "\n\t\t\t\t" . '<div class="line"><span class="time"><a href="./' . $row['identifier'] . '">' . substr($row['datetime'], -8) . '</a></span>&thinsp;' . str_replace("\n", '<br>', $row['body']) . $tagstr . '</div>';
}
$content .= "\n\t\t\t</div>";
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title><?= $tag ?> <?= $site ?></title>
		<link rel="icon" type="image/png" href="./favicon.png">
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="./css.css">
	</head>

	<body>
		<h1><a href="./"><?= $site ?></a> <?= $tag ?></h1>

		<div id="etc"></div>

		<div class="navi">
			<a href="./?tag=<?= $tag ?>&order=<?= $order ?>"><?= $order ?></a>
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
