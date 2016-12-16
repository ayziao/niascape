<?php 
$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
$now->setTimezone( new DateTimeZone('Asia/Tokyo'));

require "twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

header('Content-Type: text/html; charset=UTF-8');

//投稿
function post($now){

	$ini_array = loadIni();
	$handle = new SQLite3($ini_array['sqlite_file']); 

	$site = $_POST['site'];
	$body = str_replace("\r\n", "\n", trim($_POST['body']));
	$tags = trim($_POST['tags']);

	$tagstring = '';
	$filename = '';
	$gyazourl = '';

	$image_extension_arr = ['jpg','jpeg','gif','png'];

	if (strpos($_FILES['file']['type'],'image') !== false){ //画像投稿
		$extension = strtolower(array_pop(explode('.', $_FILES['file']['name'])));

		if (in_array($extension, $image_extension_arr)){

			$gyazoresults = gyazopost($ini_array['gyazo'],$_FILES['file']['tmp_name']); //gyazo

			$gyazourl = json_decode($gyazoresults)->permalink_url;

			$datetime = $now->format('Y-m-d H:i:s');
			$identifier = $now->format('YmdHisu');

			$results = dbinsert($handle,$site,$identifier,$datetime,$identifier,' gyazo_posted ',$gyazoresults); //gyazo投稿情報

			$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
			$now->setTimezone( new DateTimeZone('Asia/Tokyo'));
			$tagstring .= " with_image:$identifier";

			$filename = '/tmp/'.$identifier .'.'.$extension;
			move_uploaded_file($_FILES['file']['tmp_name'], $filename);
		}
	}

	$tagstringsite = '';
	if (mb_strlen($tags)){
		$tagarr = explode(' ', mb_ereg_replace('\s+', ' ', $tags));
		$tagstringsite .= ' #'.implode(' #', $tagarr); 
	}

	$datetime = $now->format('Y-m-d H:i:s');
	$identifier = $now->format('YmdHisu');

	$tagstring .= ' twitter_posted' . $tagstringsite;

	if(strlen($tagstring) > 0){
		$tagstring .= ' ';
	}


	if($body){
		$results = dbinsert($handle,$site,$identifier,$datetime,$identifier,$tagstring,$body);
	}

	// print('<pre>');
	// var_dump($_FILES);
	// var_dump($filename);
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

	if($body){
		$path = dirname(__FILE__);
		exec("nohup php -c '' '$path/multipost.php' '$site' '$identifier' '$filename' '$gyazourl'  > /dev/null &");
	}

	return;
}

//DB insert
function dbinsert($handle,$site,$identifier,$datetime,$title,$tags,$body){
	$query = <<< EOM

INSERT INTO basedata
(site,identifier,datetime,title,tags,body)
VALUES 
('$site','$identifier','$datetime','$title','$tags','$body')

EOM;
	// var_dump($query);
	return $handle->query($query); 
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
