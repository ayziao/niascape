<?php 
header('Content-Type: text/html; charset=UTF-8');
//タグ修正

$ini_array = parse_ini_file("setting.ini");
$location  = $ini_array['sqlite_file'];
$handle    = new SQLite3($location); 

$site = $_POST['site'];
$identifier = $_POST['identifier'];
$updateTags = trim($_POST['tags']);

//PENDING サイト判定いれるか
$query = <<< EOM

SELECT * 
FROM basedata 
WHERE  identifier = '$identifier'

EOM;
//AND site = '$site' 

$results = $handle->query($query); 
$row = $results->fetchArray(SQLITE3_ASSOC);

// tag取り出し
// システムタグとユーザタグ切り分け
$tagstring = '';
$tags = explode(' ',trim($row['tags']));
foreach ($tags as  $value) {
	if(strpos($value , '#') !== 0){
		$tagstring .= " $value";
	}
}


// システムタグに修正タグを組み込んで
if (mb_strlen($updateTags)){
	$tagarr = explode(' ', mb_ereg_replace('\s+', ' ', $updateTags));
	$tagstring .= ' #'.implode(' #', $tagarr); 
}

if(strlen($tagstring) > 0){
	$tagstring .= ' ';
}

// 投稿

$query = <<< EOM

UPDATE	basedata
SET	tags = '$tagstring'
WHERE	identifier = '$identifier'

EOM;
$results = $handle->query($query); 

header('Location: http://' . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"] . $identifier);

// echo '<pre>';
// var_dump('tagupdate');
// var_dump($results);
// var_dump($query);
// var_dump($tagstring);
// var_dump($_POST);
// var_dump($row);
