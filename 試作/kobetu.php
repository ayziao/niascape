<?php
/*
 * 個別ページ
 */

function vdump($obj) {
	ob_start();
	var_dump($obj);
	$dump = ob_get_contents();
	ob_end_clean();
	return $dump;
}

header('Content-Type: text/html; charset=UTF-8');

$ini_array = parse_ini_file(dirname(__FILE__) . "/setting.ini");

if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
	$site = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0];
} else {
	$site = explode("/", substr($_SERVER["SCRIPT_NAME"], 2))[0];
}
$path = array_pop(explode('/', substr($_SERVER["SCRIPT_NAME"], 1))); //リクエスト末尾から/の直後までを取得 ルーティングで末尾数字20文字判定済み前提

$command = "python3 /Volumes/data/niascape/niascape getdata";
$command .= $site ? ' --site=' . escapeshellarg($site) : '';
$command .= $path ? ' --identifier=' . escapeshellarg($path) : '';
exec($command, $out, $ret);
$row = json_decode(end($out), true);


if ($row) {
	$dump = '<pre  style="background-color: #fff;">' . "\n";
	$dump .= vdump($row);
	$dump .= vdump($_SERVER);
	$dump .= "\n</pre>";
} else {
	return false;
}

$title = $row['title'];
$tagstr = '';
$tagstr2 = '';
$systagstr = '';
$tags = explode(' ', trim($row['tags']));
foreach ($tags as $value) {
	if (strpos($value, '#') === 0) {
		$tag = substr($value, 1);
		$tagstr .= ' <a href="./?tag=' . $tag . '">' . $tag . '</a>';
		$tagstr2 .= $tag . ' ';
	} else {
		$systagstr .= "$value ";
	}
}
$tagstr2 = trim($tagstr2);
$content = $row['datetime'] . '<br><br>' . str_replace("\n", '<br>', $row['body']) . '<br><br>' . $tagstr . '<br><br>' . $systagstr;
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title><?= $title ?> <?= $site ?></title>
		<link rel="icon"       type="image/png" href="./favicon.png">
		<link rel="stylesheet" type="text/css"  href="/common.css">
		<link rel="stylesheet" type="text/css"  href="./css.css">
	</head>

	<body>
		<h1><a href="./"><?= $site ?></a> <?= $title ?></h1>

		<div id="etc"></div>

		<div style="font-size: xx-small;"> <a href="./<?= $maenohi ?>"><?= $maenohi ?></a> <a href="./<?= $tuginohi ?>"><?= $tuginohi ?></a></div>

		<div style="background-color: #fff;">

			<?= $content ?>

		</div>

		<form action="./" method="POST">
			<input type="text"   name="tags"       value="<?= $tagstr2 ?>">
			<input type="submit" name="tagUpdate"  value="タグ修正">
			<input type="hidden" name="site"       value="<?= $site ?>">
			<input type="hidden" name="identifier" value="<?= $row['identifier'] ?>">
		</form>

		<div><a href="./">top</a></div>

		<?= $dump ?>
	</body>
</html>
