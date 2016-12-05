<?php 
header('Content-Type: text/html; charset=UTF-8');
//個別ページ

function vdump($obj){
  ob_start();
  var_dump($obj);
  $dump = ob_get_contents();
  ob_end_clean();
  return $dump;
}

$ini_array = parse_ini_file("setting.ini");
$location  = $ini_array['sqlite_file'];
$handle    = new SQLite3($location); 

if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
	$site = explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0];
} else {
	$site = explode("/", substr($_SERVER["SCRIPT_NAME"],2))[0];
}
$path = array_pop(explode('/', substr($_SERVER["SCRIPT_NAME"],1)));	//リクエスト末尾から/の直後までを取得 ルーティングで末尾数字20文字判定済み前提

//PENDING サイト判定いれるか
$query = <<< EOM

SELECT * 
FROM basedata 
WHERE  identifier = '$path'

EOM;
//AND site = '$site' 

$results = $handle->query($query); 
$row = $results->fetchArray(SQLITE3_ASSOC);

if ($row) {
	$dump = '<pre  style="background-color: #fff;">'."\n";
	$dump .= vdump($query);
	$dump .= vdump($row);
	$dump .= vdump($_SERVER);
	$dump .= "\n</pre>";
} else {
	return false;
}

$title = $row['title'];
$tagstr = '';
$tags = explode(' ',trim($row['tags']));
foreach ($tags as  $value) {
	if(strpos($value , '#') === 0){
		$tag = substr($value, 1);
		$tagstr .= ' <a href="./?tag=' . $tag .'">' . $tag .'</a>';
	}
}
$content = $row['datetime'].'<br><br>'.str_replace("\n", '<br>', $row['body']).'<br><br>'.$tagstr;


?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title><?=$title?> <?=$site?></title>
		<link rel="icon" type="image/png" href="./favicon.png">
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="./css.css">
	</head>

	<body>
		<h1><a href="./"><?=$site?></a> <?=$title?></h1>

		<div id="etc"></div>

		<div style="font-size: xx-small;"> <a href="./<?=$maenohi?>"><?=$maenohi?></a> <a href="./<?=$tuginohi?>"><?=$tuginohi?></a></div>
		
		<div style="background-color: #fff;">

			<?=$content?>

		</div>

		<div><a href="./">top</a></div>

		<?=$dump?>
	</body>
</html>
