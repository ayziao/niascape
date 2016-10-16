<?php 
// タグ別投稿件数

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$user = $ini_array['default_user'];
$tag  = $_GET["tag"] ? $_GET["tag"] : $ini_array['default_tag'];


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

$handle = new SQLite3($location); 
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

$handle = new SQLite3($location); 
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
	$link .= '<a href="tagcount.php?tag='. urlencode($key) .'">' . $key . '</a> ';
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
			<a href='monthcount.php'>月別</a> <a href='daycount.php'>日別</a> <a href='weekcount.php'>曜日別</a> <a href='hourcount.php'>時別</a> タグ<br>
		<?=$link ?>

		<h4><?=$tag ?> タグ投稿件数</h4>
		<table>
			<?=$content ?>
		</table>
		<a href='monthcount.php'>月別</a> <a href='daycount.php'>日別</a> <a href='weekcount.php'>曜日別</a> <a href='hourcount.php'>時別</a> タグ
	</body>
</html>
