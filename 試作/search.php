<?php
/*
 * 検索
 */

header('Content-Type: text/html; charset=UTF-8');

$ini_array = loadIni();
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location);

if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
	$site = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0];
} else {
	$site = explode("/", substr($_SERVER["SCRIPT_NAME"], 2))[0];
}

$searchbody = $_GET['searchbody'];

$order = isset($_GET['order']) ? $_GET['order'] : 'DESC';

$query = <<< EOM

SELECT * FROM basedata
WHERE site = '$site'
AND body LIKE '%$searchbody%' 
ORDER BY identifier $order LIMIT 1000

EOM;
//ASC DESC
//print('<pre>');
//var_dump($query);

$results = $handle->query($query);
//$raw = $results->fetchArray();

$day = '';

$order = ($order == 'DESC') ? 'ASC' : 'DESC';

//TODO 時間区切りを入れる

while ($row = $results->fetchArray()) {
	$day2 = substr($row['datetime'], 0, 10);
	if ($day != $day2) {
		if ($day != '') {
			$content .= '</div>';
		}
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

	$content .= '<div class="line"><span class="time"><a href="./' . $row['identifier'] . '">18:28:18</a></span>&thinsp;' . $row['body'] . $tagstr . '</div>' . "\n";
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
