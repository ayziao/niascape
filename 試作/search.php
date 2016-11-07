<?php 
header('Content-Type: text/html; charset=UTF-8');

//検索

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location); 

if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
	$user = explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0];
} else {
	$user = explode("/", substr($_SERVER["SCRIPT_NAME"],2))[0];
}

$searchbody  = $_GET['searchbody'];

$query = <<< EOM

SELECT * FROM basedata
WHERE user = '$user'
AND body LIKE '%$searchbody%' 
ORDER BY identifier ASC LIMIT 1000

EOM;
//print('<pre>');
//var_dump($query);

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
		<title><?=$searchbody?> <?=$user?></title>
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="./css.css">
	</head>

	<body>
		<h1><?=$user?> <?=$searchbody?></h1>

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
