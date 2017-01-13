<?php
/*
 * 時別投稿件数
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

$handle = new SQLite3($location);

//今日
$query = <<< EOM
SELECT  `times`.`Date`,ifnull( `count`, 0) as 'count',`graf`
FROM 
	(SELECT strftime('%H',`datetime`) as `Date`  FROM basedata GROUP BY strftime('%H',`datetime`)) times
LEFT JOIN
(
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((count(*) + 1) / 2)), 3, count(*)), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
$bodywhere
AND DATE(`datetime`) = DATE('now', "localtime")
GROUP BY strftime('%H',`datetime`)
) counts
ON  `times`.`Date` = `counts`.`Date` 
EOM;
//var_dump($query);
$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$today .= '<tr>' . '<td nowrap>' . $row['Date'] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td>' . $row['graf'] . '</td>' . '</tr>';
}

//今週
$query = <<< EOM

SELECT t2.Date , count, graf
FROM 
(
	SELECT strftime('%H',`datetime`) as `Date`  FROM basedata GROUP BY strftime('%H',`datetime`)
) t2
LEFT JOIN
(
SELECT 
	strftime('%H',`datetime`) as `Date`,
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((count(*) + 1) / 2)), 3, count(*)), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
$bodywhere
AND strftime('%Y%W',`datetime`) = strftime('%Y%W',DATE('now', "localtime"))
GROUP BY strftime('%H',`datetime`)
) t1
ON  t1.`Date` = t2.`Date` 
EOM;

// print('<pre>');
// var_dump($query);
// print('</pre>');

$results = $handle->query($query);
while ($row = $results->fetchArray()) {
	$konsyu .= '<tr>' . '<td nowrap>' . $row['Date'] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td>' . $row['graf'] . '</td>' . '</tr>';
}


//今月
$query = <<< EOM
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((count(*) + 1) / 2)), 3, count(*)), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
$bodywhere
AND strftime('%Y-%m',`datetime`) = strftime('%Y-%m',DATE('now', "localtime"))
GROUP BY strftime('%H',`datetime`)
EOM;
//var_dump($query);
$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$kongetu .= '<tr>' . '<td nowrap>' . $row['Date'] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td>' . $row['graf'] . '</td>' . '</tr>';
}

//今年
$query = <<< EOM
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 10) + 1) / 2)), 3, (round(count(*) / 10))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
$bodywhere
AND strftime('%Y',`datetime`) = strftime('%Y',DATE('now', "localtime"))
GROUP BY strftime('%H',`datetime`)
EOM;
//var_dump($query);
$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$kotosi .= '<tr>' . '<td nowrap>' . $row['Date'] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td>' . $row['graf'] . '</td>' . '</tr>';
}


//全期間
$query = <<< EOM
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 10) + 1) / 2)), 3, (round(count(*) / 10))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
$bodywhere
GROUP BY strftime('%H',`datetime`)
EOM;
$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$zenkikan .= '<tr>' . '<td nowrap>' . $row['Date'] . '</td>' . '<td align="right">' . $row['count'] . '</td>' . '<td>' . $row['graf'] . '</td>' . '</tr>';
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

$link .= '<a href="?kanri=hourcount&site=' . $site . '">全て</a><br>';
foreach ($array as $key => $value) {
	$link .= '<a href="?kanri=hourcount&site=' . $site . '&tag=' . urlencode($key) . '">' . $key . '</a> ' . $value . '<br>';
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
	$sitelink .= '<a href="?kanri=hourcount&site=' . $row['site'] . '">' . $row['site'] . '</a> ';
}
?>
<html>
	<head>
		<title>時別投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
			.table { display: table; width: 100%; }
			.cell { display: table-cell; white-space: nowrap;}
		</style>
	</head>

	<body>
		<h4><?= $site ?> <?= $tag ?> 時別投稿件数</h4>

		<?= $sitelink ?><br>
		<a href='?kanri=monthcount&site=<?= $site ?>'>月別</a> <a href='?kanri=daycount&site=<?= $site ?>'>日別</a> <a href='?kanri=weekcount&site=<?= $site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?= $site ?>'>時別</a> <a href='?kanri=tagcount&site=<?= $site ?>'>タグ</a><br>

		<div class="table">
			<div class="cell">
				<form action="./" method="GET">
					<input type="hidden" name="kanri" value="hourcount">
					<input type="hidden" name="site" value="<?= $site ?>">
					<input type="hidden" name="tag" value="<?= $tag ?>">
					<input class="text" type="text" name="searchbody" value="<?= $searchbody ?>">
					<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
				</form>
				<?= $link ?>
			</div>
			<div class="cell" style="width: 100%;">
				<h5>今日</h5>
				<table>
					<?= $today ?>
				</table>
				<h5>今週</h5>
				<table>
					<?= $konsyu ?>
				</table>
				<h5>今月</h5>
				<table>
					<?= $kongetu ?>
				</table>
				<h5>今年</h5>
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