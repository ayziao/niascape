<?php
/*
 * 月別投稿件数
 */
header('Content-Type: text/html; charset=UTF-8');

$ini_array = parse_ini_file(dirname(__FILE__) . "/../setting.ini");
$location = $ini_array['sqlite_file'];
$site = $_GET["site"] ? $_GET["site"] : $ini_array['default_site'];
$tag = $_GET["tag"] ? $_GET["tag"] : '';
$searchbody = $_GET["searchbody"] ? $_GET["searchbody"] : '';

$command = "python3 /Volumes/data/niascape/niascape postcount.month";
$command .= $site ? ' --site='.$site : '';
$command .= $tag ? ' --tag='.$tag : '';
$command .= $searchbody ? ' --search_body='.$searchbody : '';
exec($command, $out, $ret);
$monthcount = json_decode(end($out), true);

foreach ($monthcount as $row){
	$content .= '<tr>' . '<td nowrap>' . $row['date'] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td><div style="background-color: blue;  width: ' . $row['count'] . 'px; font-size: 10px;">&nbsp;</div></td>' . '</tr>';
}

//タグ利用頻度順リンク
$command = "python3 /Volumes/data/niascape/niascape tagcount";
$command .= $site ? ' --site='.$site : '';
exec($command, $out, $ret);
$tagcount = json_decode(end($out), true);

$link .= '<a href="?kanri=daycount&site=' . $site . '">全て</a><br>';
foreach ($tagcount as $row) {
	$link .= '<a href="?kanri=daycount&site=' . $site . '&tag=' . urlencode($row['tag']) . '">' . $row['tag'] . '</a> ' . $row['count'] . '<br>';
}

//siteリンク
$command = "python3 /Volumes/data/niascape/niascape sites";
exec($command, $out, $ret);
$sites = json_decode(end($out), true);

foreach ($sites as $row) {
	$sitelink .= '<a href="?kanri=monthcount&site=' . $row['site'] . '">' . $row['site'] . '</a> ';
}

?>
<html>
	<head>
		<title>月別投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
			.table { display: table; width: 100%; }
			.cell { display: table-cell; white-space: nowrap;}
		</style>
	</head>

	<body>
		<h4><?= $site ?> <?= $tag ?> 月別投稿件数</h4>

		<?= $sitelink ?><br>
		<a href='?kanri=monthcount&site=<?= $site ?>'>月別</a> <a href='?kanri=daycount&site=<?= $site ?>'>日別</a> <a href='?kanri=weekcount&site=<?= $site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?= $site ?>'>時別</a> <a href='?kanri=tagcount&site=<?= $site ?>'>タグ</a><br>
		<div class="table">
			<div class="cell">
				<form action="./" method="GET">
					<input type="hidden" name="kanri" value="monthcount">
					<input type="hidden" name="site" value="<?= $site ?>">
					<input type="hidden" name="tag" value="<?= $tag ?>">
					<input class="text" type="text" name="searchbody" value="<?= $searchbody ?>">
					<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
				</form>
				<?= $link ?>
			</div>
			<div class="cell" style="width: 100%;">
				<table>
					<?= $content ?>
				</table>
			</div>
		</div>
		<a href='?kanri=monthcount&site=<?= $site ?>'>月別</a> <a href='?kanri=daycount&site=<?= $site ?>'>日別</a> <a href='?kanri=weekcount&site=<?= $site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?= $site ?>'>時別</a> <a href='?kanri=tagcount&site=<?= $site ?>'>タグ</a><br>
	</body>
</html>