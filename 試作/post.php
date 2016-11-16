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

	$site = $_POST['site'];
	$body = str_replace("\r\n", "\n", trim($_POST['body']));
	$tags = trim($_POST['tags']);

	$tagstring = '';

	if (strpos($_FILES['file']['type'],'image') !== false){ //画像投稿
		$gyazoresults = gyazopost($ini_array['gyazo'],$_FILES['file']['tmp_name']); //gyazo

		$datetime = $now->format('Y-m-d H:i:s');
		$identifier = $now->format('YmdHisu');

		$results = dbinsert($handle,$site,$identifier,$datetime,$identifier,' gyazo_posted ',$gyazoresults); //gyazo投稿情報

		$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
		$now->setTimezone( new DateTimeZone('Asia/Tokyo'));
		$tagstring .= " with_image:$identifier";
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
		if($_FILES['file']['tmp_name']){
		// 	twitterpost($site,$body.$tagstringsite,$_FILES['file']['tmp_name'],json_decode($gyazoresults)->permalink_url);
			$filename = '/tmp/'.$identifier;
			$gyazourl = json_decode($gyazoresults)->permalink_url;
			move_uploaded_file($_FILES['file']['tmp_name'], $filename);
		}
		exec("nohup php -c '' '../multipost.php' '$site' '$identifier' '$filename' '$gyazourl'  > /dev/null &");
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

//Twitter投稿
function twitterpost($site,$body,$filename,$gyazourl){
	//TODO 投げっぱなし裏処理にする

	$siteini = parse_ini_file("$site.ini",ture);

	if(array_key_exists('twitter_main',$siteini) == false){
		return;
	}

	$consumerKey = $siteini['twitter_main']['consumerKey'];
	$consumerSecret = $siteini['twitter_main']['consumerSecret'];
	$accessToken = $siteini['twitter_main']['accessToken'];
	$accessTokenSecret = $siteini['twitter_main']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$parameters = ['status' => $body.$siteini['twitter_main']['suffix']];

	//画像投稿
	if($siteini['twitter_main']['image'] == 'gyazo'){
		if($gyazourl){
			$parameters['status'] .= ' '.$gyazourl;
		}
	} elseif($filename){	
		$media = $twitter->upload('media/upload', ['media' => $filename]);
		$parameters['media_ids'] = $media->media_id_string;
	}

	$result = $twitter->post('statuses/update', $parameters);


	if(array_key_exists('twitter_sub',$siteini) == false){
		return;
	}

	$consumerKey = $siteini['twitter_sub']['consumerKey'];
	$consumerSecret = $siteini['twitter_sub']['consumerSecret'];
	$accessToken = $siteini['twitter_sub']['accessToken'];
	$accessTokenSecret = $siteini['twitter_sub']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$parameters = ['status' => $body.$siteini['twitter_sub']['suffix']];

	//画像投稿
	if($siteini['twitter_sub']['image'] == 'gyazo'){
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
	// var_dump($siteini);
	// var_dump($twresult);
	// var_dump($media);

	//RT ふぁぼ
	if(array_key_exists('twitter_rt',$siteini) == false){
		return;
	}
	if($siteini['twitter_rt']['noodle'] == '' or strpos($body, $siteini['twitter_rt']['noodle']) !== false){
		$consumerKey = $siteini['twitter_rt']['consumerKey'];
		$consumerSecret = $siteini['twitter_rt']['consumerSecret'];
		$accessToken = $siteini['twitter_rt']['accessToken'];
		$accessTokenSecret = $siteini['twitter_rt']['accessTokenSecret'];

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
