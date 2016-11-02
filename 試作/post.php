<?php 
$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
$now->setTimezone( new DateTimeZone('Asia/Tokyo'));

require "twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

header('Content-Type: text/html; charset=UTF-8');

//投稿
function post($now){

	$ini_array = parse_ini_file("setting.ini");
	$handle = new SQLite3($ini_array['sqlite_file']); 

	$user = $_POST['user'];
	$body = $_POST['body'];
	$tags = trim($_POST['tags']);

	$tagstring = '';

	if (strpos($_FILES['file']['type'],'image') !== false){ //画像投稿
		$gyazoresults = gyazopost($ini_array['gyazo'],$_FILES['file']['tmp_name']);

		$datetime = $now->format('Y-m-d H:i:s');
		$identifier = $now->format('YmdHisu');

		$results = dbinsert($handle,$user,$identifier,$datetime,$identifier,' gyazo_posted ',$gyazoresults);

		$tagstring .= " with_image:$identifier";

		$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
		$now->setTimezone( new DateTimeZone('Asia/Tokyo'));
	}

	if (mb_strlen($tags)){
		$tagarr = explode(' ', preg_replace('/\s+/', ' ', $tags));
		$tagstring .= ' #'.implode(' #', $tagarr); 
	}

	$datetime = $now->format('Y-m-d H:i:s');
	$identifier = $now->format('YmdHisu');

	$tagstring .= ' twitter_posted';

	if(strlen($tagstring) > 0){
		$tagstring .= ' ';
	}

	$results = dbinsert($handle,$user,$identifier,$datetime,$identifier,$tagstring,$body);


	// print('<pre>');
	// var_dump($_FILES);
	// var_dump(json_decode($gyazoresults));
	// var_dump($tags);
	// var_dump($tagarr);
	// var_dump($results);
	// var_dump($identifier);
	// var_dump($_POST);
	// var_dump($queryg);
	// var_dump($query);
	// var_dump($_SERVER);

	header('Location: http://' . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"]);

	ob_end_flush();
	ob_flush();
	flush();

	twitterpost($user,$body);

	return;
}

//DB insert
function dbinsert($handle,$user,$identifier,$datetime,$title,$tags,$body){

	$query = <<< EOM

INSERT INTO basedata
(user,identifier,datetime,title,tags,body)
VALUES 
('$user','$identifier','$datetime','$title','$tags','$body')

EOM;

	return $handle->query($query); 
}	

//Twitter投稿
function twitterpost($user,$body){
	//TODO 投げっぱなし裏処理にする
	//TODO 画像投稿

	$userini = parse_ini_file("$user.ini");

	$consumerKey = $userini['consumerKey'];
	$consumerSecret = $userini['consumerSecret'];
	$accessToken = $userini['accessToken'];
	$accessTokenSecret = $userini['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$twresult = $twitter->post("statuses/update",array("status" => $body));

	// print('<pre>');
	// var_dump($userini);
	// var_dump($twresult);
}

//gyazo投稿
function gyazopost($token,$file){

	$ch = curl_init();
	curl_setopt_array($ch, array(
	    CURLOPT_URL            => 'https://upload.gyazo.com/api/upload',
	    CURLOPT_POST           => true,
	    CURLOPT_SAFE_UPLOAD    => true,
	    CURLOPT_RETURNTRANSFER => true,
	    CURLOPT_POSTFIELDS     => array(
	        'access_token' => $token,
	        'imagedata'    => new CURLFile($file),
	    ),
	));

	$results = curl_exec($ch);

	if($errno = curl_errno($ch)) {
		var_dump($token);
		var_dump($file);
		var_dump($results);
    	$error_message = curl_strerror($errno);
    	echo "cURL error ({$errno}):\n {$error_message}";
		var_dump(curl_error());
	}
	return $results;
}


return post($now);
