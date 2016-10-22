<?php 
header('Content-Type: text/html; charset=UTF-8');

//時別投稿件数

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$user = $_GET["user"] ? $_GET["user"] : $ini_array['default_user'];
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
WHERE user = '$user' 
AND DATE(`datetime`) = DATE('now', "localtime")
GROUP BY strftime('%H',`datetime`)
) counts
ON  `times`.`Date` = `counts`.`Date` 
EOM;
//var_dump($query);
$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$today .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
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
WHERE user = '$user' 
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
	$konsyu .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}


//今月
$query = <<< EOM
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((count(*) + 1) / 2)), 3, count(*)), '0', '|') as 'graf' 
FROM basedata 
WHERE user = '$user' 
AND strftime('%Y-%m',`datetime`) = strftime('%Y-%m',DATE('now', "localtime"))
GROUP BY strftime('%H',`datetime`)
EOM;
//var_dump($query);
$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$kongetu .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}

//今年
$query = <<< EOM
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 10) + 1) / 2)), 3, (round(count(*) / 10))), '0', '|') as 'graf' 
FROM basedata 
WHERE user = '$user' 
AND strftime('%Y',`datetime`) = strftime('%Y',DATE('now', "localtime"))
GROUP BY strftime('%H',`datetime`)
EOM;
//var_dump($query);
$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$kotosi .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}


//全期間
$query = <<< EOM
SELECT 
	strftime('%H',`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((round(count(*) / 10) + 1) / 2)), 3, (round(count(*) / 10))), '0', '|') as 'graf' 
FROM basedata 
WHERE user = '$user' 
GROUP BY strftime('%H',`datetime`)
EOM;
$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$zenkikan .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
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
	$userlink .= '<a href="hourcount?user='. $row['user'].'">' . $row['user'] . '</a> ';
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
		<h4><?=$user ?> <?=$tag ?> 時別投稿件数</h4>

		<?=$userlink ?><br>
		<a href='monthcount?user=<?=$user ?>'>月別</a> <a href='daycount?user=<?=$user ?>'>日別</a> <a href='weekcount?user=<?=$user ?>'>曜日別</a> <a href='hourcount?user=<?=$user ?>'>時別</a> <a href='tagcount?user=<?=$user ?>'>タグ</a><br>
		
		<h5>今日</h5>
		<table>
			<?=$today ?>
		</table>
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