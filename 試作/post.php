<?php 
//投稿

$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
$now->setTimezone( new DateTimeZone('Asia/Tokyo'));

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location); 

$user = $_POST['user'];
$body = $_POST['body'];
$tags = trim($_POST['tags']);

$tagstring = '';//' twitter_posted’
if (mb_strlen($tags)){
	$tagarr = explode(' ', preg_replace('/\s+/', ' ', $tags));
	$tagstring .= ' #'.implode(' #', $tagarr) . ' '; 
}

$datetime = $now->format('Y-m-d H:i:s');
$identifier = $now->format('YmdHisu');

$query = <<< EOM

INSERT INTO basedata
(user,identifier,datetime,title,tags,body)
VALUES 
('$user','$identifier','$datetime','$identifier','$tagstring','$body')

EOM;

$results = $handle->query($query); 

// print('<pre>');
// var_dump($tags);
// var_dump($tagarr);
// var_dump($results);
// var_dump($identifier);
// var_dump($_POST);
// var_dump($query);
// var_dump($_SERVER);

header('Location: http://' . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"]);
