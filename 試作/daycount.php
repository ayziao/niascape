<?php 

#日別投稿件数

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$user = $ini_array['default_user'];

$query = <<< EOM
SELECT 
	DATE(`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((count(*) + 1) / 2)), 3, count(*)), '0', '|') as 'graf' 
FROM basedata 
WHERE user = '$user' 
GROUP BY DATE(`datetime`) 
ORDER BY DATE(`datetime`)  DESC
EOM;

$handle = new SQLite3($location); 
$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$content .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}

?>
<html>
	<head>
		<title>日別投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
		</style>
	</head>
	
	<body>
		<a href='monthcount.php'>月別</a> 日別 <a href='weekcount.php'>曜日別</a> <a href='hourcount.php'>時別</a> <a href='tagcount.php'>タグ</a>
		<table>
			<?=$content ?>
		</table>
		<a href='monthcount.php'>月別</a> 日別 <a href='weekcount.php'>曜日別</a> <a href='hourcount.php'>時別</a> <a href='tagcount.php'>タグ</a>
	</body>
</html>