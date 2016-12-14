<?php 
header('Content-Type: text/html; charset=UTF-8');

//日サマリー

$ini_array = loadIni();
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location); 


if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
	$site = explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0];
} else {
	$site = explode("/", substr($_SERVER["SCRIPT_NAME"],2))[0];
}

$arr  = explode('/', substr($_SERVER["SCRIPT_NAME"],1));
$path = array_pop($arr);	//リクエスト末尾から/の直後までを取得 ルーティングで末尾数字8文字判定済み前提
//$site = substr(array_pop($arr), 1); 


//前日以前取得 
$query = <<< EOM

SELECT identifier FROM basedata
WHERE site = '$site'
AND tags NOT LIKE '% gyazo_posted %'
AND identifier < '{$path}000000000000' 
ORDER BY identifier DESC LIMIT 1

EOM;
// print('<pre>');
// var_dump($query);
// var_dump($path);

$results = $handle->query($query); 

$row = $results->fetchArray(SQLITE3_ASSOC);

// var_dump($row);

$maenohi = substr($row['identifier'], 0,8);

// var_dump($maenohi);

//翌日以後取得

$query = <<< EOM

SELECT identifier FROM basedata
WHERE site = '$site'
AND tags NOT LIKE '% gyazo_posted %'
AND identifier > '{$path}999999999999' 
ORDER BY identifier ASC LIMIT 1

EOM;
// print('<pre>');
// var_dump($query);
// var_dump($path);

$results = $handle->query($query); 

$row = $results->fetchArray(SQLITE3_ASSOC);

// var_dump($row);

$tuginohi = substr($row['identifier'], 0,8);

// var_dump($tuginohi);



$query = <<< EOM

SELECT * FROM basedata
WHERE site = '$site'
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

$count = 0; //日件数
$content = "";

//TODO 時間区切りを入れる
while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	$tagstr = '';
	$tags = explode(' ',trim($row['tags']));
	foreach ($tags as  $value) {
		if(strpos($value , '#') === 0){
			$tag = substr($value, 1);
			$tagstr .= ' <a href="./?tag=' . $tag .'">' . $tag .'</a>';
		}
	}

	$content .= "\n\t\t\t\t". '<div class="line"><span class="time"><a href="./'.$row['identifier'].'">'.substr($row['datetime'], -8).'</a></span>&thinsp;'.str_replace("\n", '<br>', $row['body']).$tagstr.'</div>';

	$count++;
}

//$day = substr($row['datetime'], 0,10);
$content = "\n\t\t\t". '<h5><a href="./'. str_replace('-', '', $path).'">'.$path.'</a> '. $count.'</h5> ' ."\n\t\t\t". '<div class="lines">'.$content;
$content .= "\n\t\t\t</div>";


?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title><?=$path?> <?=$site?></title>
		<link rel="icon" type="image/png" href="./favicon.png">
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="./css.css">
	</head>

	<body>
		<h1><a href="./"><?=$site?></a> <?=$path?></h1>

		<div id="etc"></div>

		<div class="navi">
			<a href="./<?=$maenohi?>"><?=$maenohi?></a> <a href="./<?=$tuginohi?>"><?=$tuginohi?></a>
		</div>
		
		<div>

			<?=$content?>

		</div>

		<div class="navi">
			<a href="./<?=$maenohi?>"><?=$maenohi?></a> <a href="./<?=$tuginohi?>"><?=$tuginohi?></a><br>
			<a href="./">top</a>
		</div>
		<form action="./" method="GET">
			<input id="search" class="text" type="text" name="searchbody">
			<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
		</form>
	</body>
</html>
