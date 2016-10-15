<?php 

#日別投稿件数

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$user = $ini_array['default_user'];

$query = <<< EOM
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 10) + 1) / 2)), 3, (round(count(*) / 10))), '0', '|') as 'graf' 
FROM basedata 
WHERE user = '$user' 
GROUP BY strftime('%H',`datetime`)
EOM;

$handle = new SQLite3($location); 
$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$content .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}

?>
<html>
	<head>
		<title>時別投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
		</style>
	</head>
	
	<body>
		<a href='monthcount.php'>月別</a> <a href='daycount.php'>日別</a> <a href='weekcount.php'>曜日別</a> 時別 <a href='tagcount.php'>タグ</a>
		<table>
			<?=$content ?>
		</table>
		<a href='monthcount.php'>月別</a> <a href='daycount.php'>日別</a> <a href='weekcount.php'>曜日別</a> 時別 <a href='tagcount.php'>タグ</a>
	</body>
</html>