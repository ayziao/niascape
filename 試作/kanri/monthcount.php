<?php 
header('Content-Type: text/html; charset=UTF-8');

//月別投稿件数

$ini_array = parse_ini_file("../setting.ini");
$location = $ini_array['sqlite_file'];
$site = $_GET["site"] ? $_GET["site"] : $ini_array['default_site'];

$query = <<< EOM
SELECT 
	strftime('%Y-%m',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 10) + 1) / 2)), 3, (round(count(*) / 10))), '0', '|') as 'graf' 
FROM basedata 
WHERE site = '$site' 
GROUP BY strftime('%Y-%m',`datetime`)
EOM;

$handle = new SQLite3($location); 
$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$content .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
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
	$sitelink .= '<a href="?kanri=monthcount&site='. $row['site'].'">' . $row['site'] . '</a> ';
}

?>
<html>
	<head>
		<title>月別投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
		</style>
	</head>
	
	<body>
		<h4><?=$site ?> <?=$tag ?> 月別投稿件数</h4>
			
		<?=$sitelink ?><br>
		<a href='?kanri=monthcount&site=<?=$site ?>'>月別</a> <a href='?kanri=daycount&site=<?=$site ?>'>日別</a> <a href='?kanri=weekcount&site=<?=$site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?=$site ?>'>時別</a> <a href='?kanri=tagcount&site=<?=$site ?>'>タグ</a><br>
		<table>
			<?=$content ?>
		</table>
		<a href='?kanri=monthcount&site=<?=$site ?>'>月別</a> <a href='?kanri=daycount&site=<?=$site ?>'>日別</a> <a href='?kanri=weekcount&site=<?=$site ?>'>曜日別</a> <a href='?kanri=hourcount&site=<?=$site ?>'>時別</a> <a href='?kanri=tagcount&site=<?=$site ?>'>タグ</a><br>
	</body>
</html>