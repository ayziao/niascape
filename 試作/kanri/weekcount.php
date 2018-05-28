<?php
/*
 * 曜日別投稿件数
 */

header('Content-Type: text/html; charset=UTF-8');

$week = ['日', '月', '火', '水', '木', '金', '土'];
$ini_array = parse_ini_file(dirname(__FILE__) . "/../setting.ini");
$location = $ini_array['sqlite_file'];
$site = $_GET["site"] ? $_GET["site"] : $ini_array['default_site'];
$tag = $_GET["tag"] ? $_GET["tag"] : '';
$searchbody = $_GET["searchbody"] ? $_GET["searchbody"] : '';

//過去7日
$command = "python3 /Volumes/data/niascape/niascape postcount.week --past_days=7";
$command .= $site ? ' --site='.$site : '';
$command .= $tag ? ' --tag='.$tag : '';
$command .= $searchbody ? ' --search_body='.$searchbody : '';
exec($command, $out, $ret);
$weekcount = json_decode(end($out), true);

$weekcount[] = array_shift($weekcount);				
foreach ($weekcount as $row){
	$konsyu .= '<tr>' . '<td nowrap>' . $week[$row['date']] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td><div style="background-color: blue;  width: ' . $row['count'] . 'px; font-size: 10px;">&nbsp;</div></td>' . '</tr>';
}

//過去30日
$command = "python3 /Volumes/data/niascape/niascape postcount.week --past_days=30";
$command .= $site ? ' --site='.$site : '';
$command .= $tag ? ' --tag='.$tag : '';
$command .= $searchbody ? ' --search_body='.$searchbody : '';
exec($command, $out, $ret);
$weekcount = json_decode(end($out), true);

$weekcount[] = array_shift($weekcount);				
foreach ($weekcount as $row){
	$kongetu .= '<tr>' . '<td nowrap>' . $week[$row['date']] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td><div style="background-color: blue;  width: ' . $row['count'] . 'px; font-size: 10px;">&nbsp;</div></td>' . '</tr>';
}

//過去365日
$command = "python3 /Volumes/data/niascape/niascape postcount.week --past_days=365";
$command .= $site ? ' --site='.$site : '';
$command .= $tag ? ' --tag='.$tag : '';
$command .= $searchbody ? ' --search_body='.$searchbody : '';
exec($command, $out, $ret);
$weekcount = json_decode(end($out), true);

$weekcount[] = array_shift($weekcount);				
foreach ($weekcount as $row){
	$kotosi .= '<tr>' . '<td nowrap>' . $week[$row['date']] . '</td>' . '<td align="right">' . $row['count'] . '</td>' ;
	if ($site == 'rog') {
		$row['count'] = $row['count'] / 3;
	}
	$kotosi .= '<td><div style="background-color: blue;  width: ' . $row['count'] . 'px; font-size: 10px;">&nbsp;</div></td>' . '</tr>';
}

//全期間
$command = "python3 /Volumes/data/niascape/niascape postcount.week";
$command .= $site ? ' --site='.$site : '';
$command .= $tag ? ' --tag='.$tag : '';
$command .= $searchbody ? ' --search_body='.$searchbody : '';
exec($command, $out, $ret);
$weekcount = json_decode(end($out), true);

$weekcount[] = array_shift($weekcount);				
foreach ($weekcount as $row){
	$zenkikan .= '<tr>' . '<td nowrap>' . $week[$row['date']] . '</td>' . '<td align="right">' . $row['count'] . '</td>' ;
	if ($site == 'rog') {
		$row['count'] = $row['count'] / 20;
	}
	$zenkikan .= '<td><div style="background-color: blue;  width: ' . $row['count'] . 'px; font-size: 10px;">&nbsp;</div></td>' . '</tr>';
}

//タグ利用頻度順リンク
$command = "python3 /Volumes/data/niascape/niascape postcount.tag";
$command .= $site ? ' --site='.$site : '';
exec($command, $out, $ret);
$tagcount = json_decode(end($out), true);

$link .= '<a href="?kanri=weekcount&site=' . $site . '">全て</a><br>';
foreach ($tagcount as $row) {
	$link .= '<a href="?kanri=weekcount&site=' . $site . '&tag=' . urlencode($row['tag']) . '">' . $row['tag'] . '</a> ' . $row['count'] . '<br>';
}

//siteリンク
$command = "python3 /Volumes/data/niascape/niascape site.list";
exec($command, $out, $ret);
$sites = json_decode(end($out), true);

foreach ($sites as $row) {
	$sitelink .= '<a href="?kanri=weekcount&site=' . $row['site'] . '">' . $row['site'] . '</a> ';
}

?>
<html>
	<head>
		<title>曜日別投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
			.table { display: table; width: 100%; }
			.cell { display: table-cell; white-space: nowrap;}
		</style>
	</head>

	<body>
		<h4><?= $site ?> <?= $tag ?> 曜日別投稿件数</h4>

		<?= $sitelink ?><br>
		<a href='?kanri=monthcount&site=<?= $site ?>'>月別</a> <a href='?kanri=daycount&site=<?= $site ?>'>日別</a> <a href='?kanri=weekcount&site=<?= $site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?= $site ?>'>時別</a> <a href='?kanri=tagcount&site=<?= $site ?>'>タグ</a><br>
		<div class="table">
			<div class="cell">
				<form action="./" method="GET">
					<input type="hidden" name="kanri" value="weekcount">
					<input type="hidden" name="site" value="<?= $site ?>">
					<input type="hidden" name="tag" value="<?= $tag ?>">
					<input class="text" type="text" name="searchbody" value="<?= $searchbody ?>">
					<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
				</form>
				<?= $link ?>
			</div>
			<div class="cell" style="width: 100%;">
				<h5>過去7日</h5>
				<table>
					<?= $konsyu ?>
				</table>
				<h5>過去30日</h5>
				<table>
					<?= $kongetu ?>
				</table>
				<h5>過去365日</h5>
				<table>
					<?= $kotosi ?>
				</table>
				<h5>全期間</h5>
				<table>
					<?= $zenkikan ?>
				</table>
			</div>
		</div>		

		<a href='?kanri=monthcount&site=<?= $site ?>'>月別</a> <a href='?kanri=daycount&site=<?= $site ?>'>日別</a> <a href='?kanri=weekcount&site=<?= $site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?= $site ?>'>時別</a> <a href='?kanri=tagcount&site=<?= $site ?>'>タグ</a><br>
	</body>
</html>