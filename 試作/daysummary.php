<?php 
header('Content-Type: text/html; charset=UTF-8');

//日サマリー

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location); 

$arr  = explode('/', substr($_SERVER["SCRIPT_NAME"],1));
$path = array_pop($arr);	//リクエスト末尾から/の直後までを取得 ルーティングで末尾数字8文字判定済み前提
$user = substr(array_pop($arr), 1); 

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
			$content .= '</div>';
		}
		$content .= '<h5><a href="./'. str_replace('-', '', $day2).'">'.$day2.'</a></h5><div class="lines">';
		$day = $day2;
	}

	$tagstr = '';
	$tags = explode(' ',trim($row['tags']));
	foreach ($tags as  $value) {
		if(strpos($value , '#') === 0){
			$tag = substr($value, 1);
			$tagstr .= ' <a href="./?tag=' . $tag .'">' . $tag .'<a>';
		}
	}

	$content .= '<div class="line"><span class="time"><a href="./'.$row['identifier'].'">18:28:18</a></span>&thinsp;'.$row['body'].$tagstr.'</div>'."\n";
}
$content .= '</div>';

?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title><?=$path?> <?=$user?></title>
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="/css.css">
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
