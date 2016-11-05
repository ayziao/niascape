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
		$gyazoresults = gyazopost($ini_array['gyazo'],$_FILES['file']['tmp_name']); //gyazo

		$datetime = $now->format('Y-m-d H:i:s');
		$identifier = $now->format('YmdHisu');

		$results = dbinsert($handle,$user,$identifier,$datetime,$identifier,' gyazo_posted ',$gyazoresults); //gyazo投稿情報

		$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
		$now->setTimezone( new DateTimeZone('Asia/Tokyo'));
		$tagstring .= " with_image:$identifier";
	}

	$tagstringuser = '';
	if (mb_strlen($tags)){
		$tagarr = explode(' ', preg_replace('/\s+/', ' ', $tags));
		$tagstringuser .= ' #'.implode(' #', $tagarr); 
	}

	$datetime = $now->format('Y-m-d H:i:s');
	$identifier = $now->format('YmdHisu');

	$tagstring .= ' twitter_posted' + $tagstringuser;

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

	twitterpost($user,$body.$tagstringuser,$_FILES['file']['tmp_name'],json_decode($gyazoresults)->permalink_url);

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
function twitterpost($user,$body,$filename,$gyazourl){
	//TODO 投げっぱなし裏処理にする

	$userini = parse_ini_file("$user.ini",ture);

	if(array_key_exists('twitter_main',$userini) == false){
		return;
	}

	$consumerKey = $userini['twitter_main']['consumerKey'];
	$consumerSecret = $userini['twitter_main']['consumerSecret'];
	$accessToken = $userini['twitter_main']['accessToken'];
	$accessTokenSecret = $userini['twitter_main']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$parameters = ['status' => $body.$userini['twitter_main']['suffix']];

	//画像投稿
	if($userini['twitter_main']['image'] == 'gyazo'){
		if($gyazourl){
			$parameters['status'] .= ' '.$gyazourl;
		}
	} elseif($filename){	
		$media = $twitter->upload('media/upload', ['media' => $filename]);
		$parameters['media_ids'] = $media->media_id_string;
	}

	$result = $twitter->post('statuses/update', $parameters);


	if(array_key_exists('twitter_sub',$userini) == false){
		return;
	}

	$consumerKey = $userini['twitter_sub']['consumerKey'];
	$consumerSecret = $userini['twitter_sub']['consumerSecret'];
	$accessToken = $userini['twitter_sub']['accessToken'];
	$accessTokenSecret = $userini['twitter_sub']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$parameters = ['status' => $body.$userini['twitter_sub']['suffix']];

	//画像投稿
	if($userini['twitter_sub']['image'] == 'gyazo'){
		if($gyazourl){
			$parameters['status'] .= ' '.$gyazourl;
		}
	} elseif($filename){	
		$media = $twitter->upload('media/upload', ['media' => $filename]);
		$parameters['media_ids'] = $media->media_id_string;
	}

	$result2 = $twitter->post('statuses/update', $parameters);


	// print('<pre>');
	// var_dump($result);
	// var_dump($result2);
	// var_dump($userini);
	// var_dump($twresult);
	// var_dump($media);

	//RT ふぁぼ
	if(array_key_exists('twitter_rt',$userini) == false){
		return;
	}
	if($userini['twitter_rt']['noodle'] == '' or strpos($body, $userini['twitter_rt']['noodle']) !== false){
		$consumerKey = $userini['twitter_rt']['consumerKey'];
		$consumerSecret = $userini['twitter_rt']['consumerSecret'];
		$accessToken = $userini['twitter_rt']['accessToken'];
		$accessTokenSecret = $userini['twitter_rt']['accessTokenSecret'];

		$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);
		$result3 = $twitter->post('favorites/create', ['id' => $result->id_str]);
		$result4 = $twitter->post('statuses/retweet', ['id' => $result->id_str]);
	}
	// var_dump($result3);
	// var_dump($result4);

	return $result;
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
