<?php
/* マルチポスト

exec("nohup php -c '' 'multipost.php' 'site' 'id' > /dev/null &");

*/

date_default_timezone_set('Asia/Tokyo');
$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
$now->setTimezone( new DateTimeZone('Asia/Tokyo'));

require "twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

//Twitter投稿
function twitterpost($sitesetting,$site,$body,$filename,$gyazourl){

	if(array_key_exists('twitter_main',$sitesetting) == false){
		return;
	}

	$consumerKey = $sitesetting['twitter_main']['consumerKey'];
	$consumerSecret = $sitesetting['twitter_main']['consumerSecret'];
	$accessToken = $sitesetting['twitter_main']['accessToken'];
	$accessTokenSecret = $sitesetting['twitter_main']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$parameters = ['status' => $body.$sitesetting['twitter_main']['suffix']];

	//画像投稿
	if($sitesetting['twitter_main']['image'] == 'gyazo'){
		if($gyazourl){
			$parameters['status'] .= ' '.$gyazourl;
		}
	} elseif($filename){	
		$media = $twitter->upload('media/upload', ['media' => $filename]);
		$parameters['media_ids'] = $media->media_id_string;
	}

	$result = $twitter->post('statuses/update', $parameters);

	if(array_key_exists('twitter_sub',$sitesetting) == false){
		return;
	}

	$consumerKey = $sitesetting['twitter_sub']['consumerKey'];
	$consumerSecret = $sitesetting['twitter_sub']['consumerSecret'];
	$accessToken = $sitesetting['twitter_sub']['accessToken'];
	$accessTokenSecret = $sitesetting['twitter_sub']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$parameters = ['status' => $result->text.$sitesetting['twitter_sub']['suffix']];

	//画像投稿
	if($sitesetting['twitter_sub']['image'] == 'gyazo'){
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
	// var_dump($sitesetting);
	// var_dump($twresult);
	// var_dump($media);

	//RT ふぁぼ
	if(array_key_exists('twitter_rt',$sitesetting) == false){
		return;
	}
	if($sitesetting['twitter_rt']['noodle'] == '' or strpos($body, $sitesetting['twitter_rt']['noodle']) !== false){
		$consumerKey = $sitesetting['twitter_rt']['consumerKey'];
		$consumerSecret = $sitesetting['twitter_rt']['consumerSecret'];
		$accessToken = $sitesetting['twitter_rt']['accessToken'];
		$accessTokenSecret = $sitesetting['twitter_rt']['accessTokenSecret'];

		$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);
		$result3 = $twitter->post('favorites/create', ['id' => $result->id_str]);
		$result4 = $twitter->post('statuses/retweet', ['id' => $result->id_str]);
	}
	// var_dump($result3);
	// var_dump($result4);

	return $result;
}

echo "multipost\n";
//sleep(2);

$ini_array = parse_ini_file("setting.ini");
$location  = $ini_array['sqlite_file'];
$handle    = new SQLite3($location); 

//var_dump($ini_array);
//var_dump($argv);

//コマンドライン引数受取
$site = trim($argv[1]);
$id = trim($argv[2]);
$filename = trim($argv[3]);
$gyazourl = trim($argv[4]);

//DB読み出し
$query = <<< EOM

SELECT * 
FROM basedata 
WHERE  identifier = '$id'

EOM;
//AND site = '$site'  //PENDING サイト判定いれるか
//var_dump($query);
$results = $handle->query($query); 
$raw = $results->fetchArray();

$body = $raw['body'];
$tags = $raw['tags'];
$sitesetting = getSitesetting($handle,$site);
$handle->close();

//TODO 画像どうにか

//echo "hoge\n";
//var_dump($tags);

$tagarr = explode(' ', trim($tags));
$tagstr = '';
foreach ($tagarr as $key => $value) {
	if(strpos($value, '#') === 0){
		$tagstr.= ' '.$value;
	}
}

//Twitter投稿
if ($body){
	twitterpost($sitesetting,$site,$body.$tagstr,$filename,$gyazourl);
}

echo "done\n";




function getSitesetting($handle,$site){

	$query = <<< EOM

SELECT * FROM keyvalue	
WHERE key = 'sitesetting_$site'

EOM;

	$results = $handle->query($query); 
	$row = $results->fetchArray();

	return json_decode($row['value'],ture);
}

