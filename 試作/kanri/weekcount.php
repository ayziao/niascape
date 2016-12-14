<?php
header('Content-Type: text/html; charset=UTF-8');
	
//曜日別投稿件数

$week = ['日','月','火','水','木','金','土'];
$ini_array = loadIni();
$location = $ini_array['sqlite_file'];
$site  = $_GET["site"] ? $_GET["site"] : $ini_array['default_site'];
$tag  = $_GET["tag"] ? $_GET["tag"] : '';

if ($tag){
	$tagwhere = "	and (tags like '% $tag %' or tags like '% $tag:%')";
}

$handle = new SQLite3($location); 

//今週
$query = <<< EOM
SELECT t2.Date , count, graf
FROM
(
SELECT 
	strftime('%w',`datetime`) as `Date` 
FROM basedata 
WHERE site = '$site' 
GROUP BY strftime('%w',`datetime`)
) t2
LEFT JOIN
(
SELECT 
	strftime('%w',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 5) + 1) / 2)), 3, (round(count(*) / 5))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
AND strftime('%Y%W',`datetime`) = strftime('%Y%W',DATE('now', "localtime"))
GROUP BY strftime('%w',`datetime`)
) t1
ON  t1.`Date` = t2.`Date` 
EOM;

// print('<pre>');
// var_dump($query);
// print('</pre>');

$results = $handle->query($query); 

$sun = $results->fetchArray();
while ($row = $results->fetchArray()) {
	$konsyu .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}
$row = $sun;
$konsyu .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>' . "\n\n";


//今月
$query = <<< EOM
SELECT 
	strftime('%w',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 5) + 1) / 2)), 3, (round(count(*) / 5))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
AND strftime('%Y%m',`datetime`) = strftime('%Y%m',DATE('now', "localtime"))
GROUP BY strftime('%w',`datetime`)
EOM;
$results = $handle->query($query); 

$sun = $results->fetchArray();
while ($row = $results->fetchArray()) {
	$kongetu .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}
$row = $sun;
$kongetu .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>' . "\n\n";


//今年
$query = <<< EOM
SELECT 
	strftime('%w',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 20) + 1) / 2)), 3, (round(count(*) / 20))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
AND strftime('%Y',`datetime`) = strftime('%Y',DATE('now', "localtime"))
GROUP BY strftime('%w',`datetime`)
EOM;
$results = $handle->query($query); 

$sun = $results->fetchArray();
while ($row = $results->fetchArray()) {
	$kotosi .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}
$row = $sun;
$kotosi .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>' . "\n\n";




//全期間
$query = <<< EOM
SELECT 
	strftime('%w',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 20) + 1) / 2)), 3, (round(count(*) / 20))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
$tagwhere 
GROUP BY strftime('%w',`datetime`)
EOM;
$results = $handle->query($query); 

$sun = $results->fetchArray();
while ($row = $results->fetchArray()) {
	$zenkikan .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}
$row = $sun;
$zenkikan .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>' . "\n\n";

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
	$tags = explode(" ", str_replace("\t",' ',trim($row['tags'])));
	foreach ($tags as $value) {
		$aaa = mb_strstr($value,':',ture)?mb_strstr($value,':',ture):$value; //スペースで切り離し
		$array[$aaa] += $row['count']; //件数足し足し
	}
	ksort($array);
	arsort($array);
}

$link .= '<a href="?kanri=weekcount&site='. $site. '">全て</a><br>';
foreach ($array as $key => $value) {
	$link .= '<a href="?kanri=weekcount&site='. $site.'&tag='. urlencode($key) .'">' . $key . '</a> '.$value.'<br>';
}


//siteリンク
$query = <<< EOM
SELECT site,COUNT(*)
FROM basedata 
GROUP BY site
ORDER BY COUNT(*) DESC
EOM;

$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$sitelink .= '<a href="?kanri=weekcount&site='. $row['site'].'">' . $row['site'] . '</a> ';
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
		<h4><?=$site ?> <?=$tag ?> 曜日別投稿件数</h4>
			
		<?=$sitelink ?><br>
		<a href='?kanri=monthcount&site=<?=$site ?>'>月別</a> <a href='?kanri=daycount&site=<?=$site ?>'>日別</a> <a href='?kanri=weekcount&site=<?=$site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?=$site ?>'>時別</a> <a href='?kanri=tagcount&site=<?=$site ?>'>タグ</a><br>
		<div class="table">
			<div class="cell">
				<?=$link ?>
			</div>
			<div class="cell" style="width: 100%;">
				<h5>今週</h5>
				<table>
					<?=$konsyu ?>
				</table>
				<h5>今月</h5>
				<table>
					<?=$kongetu ?>
				</table>
				<h5>今年</h5>
				<table>
					<?=$kotosi ?>
				</table>
				<h5>全期間</h5>
				<table>
					<?=$zenkikan ?>
				</table>
			</div>
		</div>		

		<a href='?kanri=monthcount&site=<?=$site ?>'>月別</a> <a href='?kanri=daycount&site=<?=$site ?>'>日別</a> <a href='?kanri=weekcount&site=<?=$site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?=$site ?>'>時別</a> <a href='?kanri=tagcount&site=<?=$site ?>'>タグ</a><br>
	</body>
</html>