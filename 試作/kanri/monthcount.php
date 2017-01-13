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

if ($tag) {
	$tagwhere = "	and (tags like '% $tag %' or tags like '% $tag:%')";
}
if ($searchbody) {
	$bodywhere = "	AND body LIKE '%$searchbody%'";
}

$query = <<< EOM
SELECT 
	strftime('%Y-%m',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 10) + 1) / 2)), 3, (round(count(*) / 10))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
$bodywhere
GROUP BY strftime('%Y-%m',`datetime`)
EOM;


$handle = new SQLite3($location);
$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$content .= '<tr>' . '<td nowrap>' . $row['Date'] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td>' . $row['graf'] . '</td>' . '</tr>';
}

//タグ利用頻度順リンク
//タグ件数取得

$query = <<< EOM
SELECT 
	tags ,
	COUNT(*) as 'count'
FROM basedata 
WHERE
	site = '$site'
GROUP BY tags
ORDER BY COUNT(*) DESC
EOM;
//, replace(substr(quote(zeroblob((count(*) + 1) / 2)), 3, count(*)), '0', '|') as 'graf' 

$results = $handle->query($query);
$array = [];
while ($row = $results->fetchArray()) {
	$tags = explode(" ", str_replace("\t", ' ', trim($row['tags'])));
	foreach ($tags as $value) {
		$aaa = mb_strstr($value, ':', ture) ? mb_strstr($value, ':', ture) : $value; //スペースで切り離し
		$array[$aaa] += $row['count']; //件数足し足し
	}
	ksort($array);
	arsort($array);
}

$link .= '<a href="?kanri=monthcount&site=' . $site . '">全て</a><br>';
foreach ($array as $key => $value) {
	$link .= '<a href="?kanri=monthcount&site=' . $site . '&tag=' . urlencode($key) . '">' . $key . '</a> ' . $value . '<br>';
}


//siteリンク

$query = <<< EOM
SELECT 
	site
	, COUNT(*)
FROM basedata 
GROUP BY site
ORDER BY COUNT(*) DESC
EOM;

$results = $handle->query($query);

while ($row = $results->fetchArray()) {
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