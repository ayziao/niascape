<?php 
//日別投稿件数

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$user  = $_GET["user"] ? $_GET["user"] : $ini_array['default_user'];

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


//userリンク

$query = <<< EOM
SELECT 
	user
	, COUNT(*)
FROM basedata 
GROUP BY user
ORDER BY COUNT(*) DESC
EOM;

$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$userlink .= '<a href="daycount.php?user='. $row['user'].'">' . $row['user'] . '</a> ';
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
		<h4><?=$user ?> <?=$tag ?> 日別投稿件数</h4>

		<?=$userlink ?><br>
		<a href='monthcount.php?user=<?=$user ?>'>月別</a> <a href='daycount.php?user=<?=$user ?>'>日別</a> <a href='weekcount.php?user=<?=$user ?>'>曜日別</a> <a href='hourcount.php?user=<?=$user ?>'>時別</a> <a href='tagcount.php?user=<?=$user ?>'>タグ</a><br>
		<table>
			<?=$content ?>
		</table>
		<a href='monthcount.php?user=<?=$user ?>'>月別</a> <a href='daycount.php?user=<?=$user ?>'>日別</a> <a href='weekcount.php?user=<?=$user ?>'>曜日別</a> <a href='hourcount.php?user=<?=$user ?>'>時別</a> <a href='tagcount.php?user=<?=$user ?>'>タグ</a><br>
	</body>
</html>