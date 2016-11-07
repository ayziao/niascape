<?php 
header('Content-Type: text/html; charset=UTF-8');

//日サマリー

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location); 


if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
	$user = explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0];
} else {
	$user = explode("/", substr($_SERVER["SCRIPT_NAME"],2))[0];
}

$arr  = explode('/', substr($_SERVER["SCRIPT_NAME"],1));
$path = array_pop($arr);	//リクエスト末尾から/の直後までを取得 ルーティングで末尾数字8文字判定済み前提
//$user = substr(array_pop($arr), 1); 

$query = <<< EOM

SELECT * FROM basedata
WHERE user = '$user'
AND tags NOT LIKE '% gyazo_posted %'
AND title LIKE '$path%' 
ORDER BY identifier ASC LIMIT 1000

EOM;
//PENDING タイトル無しで投稿して自動で日時タイトルになったやつしかとってきてない	
//print('<pre>');
//var_dump($query);
//var_dump($raw);
$results = $handle->query($query); 
//$raw = $results->fetchArray();

$day = '';

//TODO 時間区切りを入れる

while ($row = $results->fetchArray()) {
	$day2 = substr($row['datetime'], 0,10);
	if($day != $day2){
		if($day != ''){
			$content .= "\n\t\t\t</div>";
		}
		$content .= "\n\t\t\t". '<h5><a href="./'. str_replace('-', '', $day2).'">'.$day2.'</a></h5> '. "\n\t\t\t". '<div class="lines">';
		$day = $day2;
	}

	$tagstr = '';
	$tags = explode(' ',trim($row['tags']));
	foreach ($tags as  $value) {
		if(strpos($value , '#') === 0){
			$tag = substr($value, 1);
			$tagstr .= ' <a href="./?tag=' . $tag .'">' . $tag .'</a>';
		}
	}

	$content .= "\n\t\t\t\t". '<div class="line"><span class="time"><a href="./'.$row['identifier'].'">'.substr($row['datetime'], -8).'</a></span>&thinsp;'.str_replace("\n", '<br>', $row['body']).$tagstr.'</div>';
}
$content .= "\n\t\t\t</div>";

?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title><?=$path?> <?=$user?></title>
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="./css.css">
	</head>

	<body>
		<h1><?=$user?> <?=$path?></h1>

		<div id="etc"></div>
		
		<div>

			<?=$content?>

		</div>

		<div><a href="./">top</a></div>
		<form action="./" method="GET">
			<input id="search" class="text" type="text" name="searchbody">
			<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
		</form>
	</body>
</html>
