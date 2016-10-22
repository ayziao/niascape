<?php
header('Content-Type: text/html; charset=UTF-8');
	
//曜日別投稿件数

$week = ['日','月','火','水','木','金','土'];
$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$user  = $_GET["user"] ? $_GET["user"] : $ini_array['default_user'];
$handle = new SQLite3($location); 

//今週
$query = <<< EOM
SELECT t2.Date , count, graf
FROM
(
SELECT 
	strftime('%w',`datetime`) as `Date` 
FROM basedata 
WHERE user = '$user' 
GROUP BY strftime('%w',`datetime`)
) t2
LEFT JOIN
(
SELECT 
	strftime('%w',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 5) + 1) / 2)), 3, (round(count(*) / 5))), '0', '|') as 'graf' 
FROM basedata 
WHERE user = '$user' 
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
WHERE user = '$user' 
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
WHERE user = '$user' 
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
WHERE user = '$user' 
GROUP BY strftime('%w',`datetime`)
EOM;
$results = $handle->query($query); 

$sun = $results->fetchArray();
while ($row = $results->fetchArray()) {
	$zenkikan .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}
$row = $sun;
$zenkikan .= "\n			" . '<tr>'.'<td nowrap>'.$week[$row['Date']].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>' . "\n\n";


//userリンク
$query = <<< EOM
SELECT user,COUNT(*)
FROM basedata 
GROUP BY user
ORDER BY COUNT(*) DESC
EOM;

$results = $handle->query($query);

while ($row = $results->fetchArray()) {
	$userlink .= '<a href="weekcount?user='. $row['user'].'">' . $row['user'] . '</a> ';
}

?>
<html>
	<head>
		<title>曜日別投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
		</style>
	</head>

	<body>
		<h4><?=$user ?> <?=$tag ?> 曜日別投稿件数</h4>
			
		<?=$userlink ?><br>
		<a href='monthcount?user=<?=$user ?>'>月別</a> <a href='daycount?user=<?=$user ?>'>日別</a> <a href='weekcount?user=<?=$user ?>'>曜日別</a> <a href='hourcount?user=<?=$user ?>'>時別</a> <a href='tagcount?user=<?=$user ?>'>タグ</a><br>
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
		<a href='monthcount?user=<?=$user ?>'>月別</a> <a href='daycount?user=<?=$user ?>'>日別</a> <a href='weekcount?user=<?=$user ?>'>曜日別</a> <a href='hourcount?user=<?=$user ?>'>時別</a> <a href='tagcount?user=<?=$user ?>'>タグ</a><br>
	</body>
</html>