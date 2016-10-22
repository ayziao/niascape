<?php 
header('Content-Type: text/html; charset=UTF-8');

// タグ別投稿件数

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$user  = $_GET["user"] ? $_GET["user"] : $ini_array['default_user'];
$tag  = $_GET["tag"] ? $_GET["tag"] : $ini_array['default_tag'];
$handle = new SQLite3($location); 


$query = <<< EOM
SELECT 
	DATE(`datetime`) as `Date` , 
	COUNT(*) as 'count',
	replace(substr(quote(zeroblob((count(*) + 1) / 2)), 3, count(*)), '0', '|') as 'graf' 
FROM basedata 
WHERE
	user = '$user'
	and tags like '% $tag %'
GROUP BY DATE(`datetime`) 
ORDER BY DATE(`datetime`)  DESC
EOM;

$results = $handle->query($query); 

while ($row = $results->fetchArray()) {
	$content .= '<tr>'.'<td nowrap>'.$row['Date'].'</td>'.'<td align="right">'.$row['count'].'</td>'.'<td>'.$row['graf'].'</td>'.'</tr>';
}

//タグ利用頻度順リンク
//タグ件数取得

$query = <<< EOM
SELECT 
	tags ,
	COUNT(*) as 'count'
FROM basedata 
WHERE
	user = '$user'
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

foreach ($array as $key => $value) {
	$link .= '<a href="tagcount?user='. $user.'&tag='. urlencode($key) .'">' . $key . '</a> ';
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
	$userlink .= '<a href="tagcount?user='. $row['user'].'">' . $row['user'] . '</a> ';
}


?>
<html>
	<head>
		<title><?=$tag ?> タグ投稿件数</title>
		<style type="text/css">
			table {
				font-size: 70%;
			}
		</style>
	</head>
	
	<body>
		<h4><?=$user ?> <?=$tag ?> タグ投稿件数</h4>
			
		<?=$userlink ?><br>
		<a href='monthcount?user=<?=$user ?>'>月別</a> <a href='daycount?user=<?=$user ?>'>日別</a> <a href='weekcount?user=<?=$user ?>'>曜日別</a> <a href='hourcount?user=<?=$user ?>'>時別</a> <a href='tagcount?user=<?=$user ?>'>タグ</a><br>
		<?=$link ?>

		<table>
			<?=$content ?>
		</table>
		<a href='monthcount?user=<?=$user ?>'>月別</a> <a href='daycount?user=<?=$user ?>'>日別</a> <a href='weekcount?user=<?=$user ?>'>曜日別</a> <a href='hourcount?user=<?=$user ?>'>時別</a> <a href='tagcount?user=<?=$user ?>'>タグ</a><br>
	</body>
</html>
