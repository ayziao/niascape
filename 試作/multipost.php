<?php
/*
 *  マルチポスト
 * 

  exec("nohup php -c '' 'multipost.php' '$site' '$identifier' '$filename' '$gyazourl'  > /dev/null &");

 */

//ini_set( 'error_reporting', E_ALL );
function shutdown() {
	echo "\033[0m";
}

echo "\033[0;31m";
register_shutdown_function('shutdown');

function consoleLog($str) {
	echo ("\033[0m$str\n\033[0;31m");
}

function console_var_dump($var) {
	echo "\033[0m";
	var_dump($var);
	echo "\033[0;31m";
}

date_default_timezone_set('Asia/Tokyo');
require "lib/twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

$now = \DateTime::createFromFormat('U.u', sprintf('%6F', microtime(true)));
$now->setTimezone(new DateTimeZone('Asia/Tokyo'));

consoleLog("multipost");

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location);

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
$sitesetting = getSitesetting($handle, $site);
$handle->close();

//TODO 画像どうにか
//echo "hoge\n";
//var_dump($tags);

$tagarr = explode(' ', trim($tags));
$tagstr = '';
foreach ($tagarr as $key => $value) {
	if (strpos($value, '#') === 0) {
		$tagstr .= ' ' . $value;
	}
}

//Twitter投稿
if ($body) {
	twitterpost($sitesetting, $site, $body . $tagstr, $filename, $gyazourl);
	if($site == 'rog'){
		mastodonpost($body . $tagstr . ' ' . $gyazourl);
	}
}

consoleLog("done");

//Twitter投稿
function twitterpost($sitesetting, $site, $body, $filename, $gyazourl) {

	//PENDING 設定の保存の仕方考える
	$pre = $sitesetting['pre'];
	$word_list = $sitesetting['preword'];
	console_var_dump($sitesetting);
//	console_var_dump(json_encode($sitesetting,JSON_PRETTY_PRINT));

	str_replace($word_list, "", $body, $count);
	if ($count !== 0) {
		$body = $pre . $body;
	}

	if (array_key_exists('twitter_main', $sitesetting) == false) {
		return;
	}

	$consumerKey = $sitesetting['twitter_main']['consumerKey'];
	$consumerSecret = $sitesetting['twitter_main']['consumerSecret'];
	$accessToken = $sitesetting['twitter_main']['accessToken'];
	$accessTokenSecret = $sitesetting['twitter_main']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	$parameters = ['status' => $body . $sitesetting['twitter_main']['suffix']];

	//画像投稿
	if ($sitesetting['twitter_main']['image'] == 'gyazo') {
		if ($gyazourl) {
			$parameters['status'] .= ' ' . $gyazourl;
		}
	} elseif ($filename) {
		$media = $twitter->upload('media/upload', ['media' => $filename]);
		$parameters['media_ids'] = $media->media_id_string;
	}

	$result = $twitter->post('statuses/update', $parameters);
	console_var_dump($result);

	if (array_key_exists('twitter_sub', $sitesetting) == false) {
		return;
	}

	$consumerKey = $sitesetting['twitter_sub']['consumerKey'];
	$consumerSecret = $sitesetting['twitter_sub']['consumerSecret'];
	$accessToken = $sitesetting['twitter_sub']['accessToken'];
	$accessTokenSecret = $sitesetting['twitter_sub']['accessTokenSecret'];

	$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

	//PENDING 接頭と画像をうまいことやる
	$body = preg_replace("/^$pre/", '', $result->text);

	$parameters = ['status' => $body . $sitesetting['twitter_sub']['suffix']];

	//画像投稿
	if ($sitesetting['twitter_sub']['image'] == 'gyazo') {
		if ($gyazourl) {
			$parameters['status'] .= ' ' . $gyazourl;
		}
	} elseif ($filename) {
		$media = $twitter->upload('media/upload', ['media' => $filename]);
		$parameters['media_ids'] = $media->media_id_string;
		console_var_dump($media);
	}

	$result2 = $twitter->post('statuses/update', $parameters);
	console_var_dump($result2);


	//RT ふぁぼ
	if (array_key_exists('twitter_rt', $sitesetting) == false) {
		return;
	}
	if ($sitesetting['twitter_rt']['noodle'] == '' or strpos($body, $sitesetting['twitter_rt']['noodle']) !== false) {
		$consumerKey = $sitesetting['twitter_rt']['consumerKey'];
		$consumerSecret = $sitesetting['twitter_rt']['consumerSecret'];
		$accessToken = $sitesetting['twitter_rt']['accessToken'];
		$accessTokenSecret = $sitesetting['twitter_rt']['accessTokenSecret'];

		$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);
		$result3 = $twitter->post('favorites/create', ['id' => $result->id_str]);
		$result4 = $twitter->post('statuses/retweet', ['id' => $result->id_str]);
		console_var_dump($result3);
		console_var_dump($result4);
	}

	return $result;
}


function mastodonpost($body){
//	require_once("autoload.php");
	
	require "lib/theCodingCompany/Mastodon.php";
	$t = new \theCodingCompany\Mastodon();
	//Toot Test
	$statusses = $t->PostStatuses($body);
	var_dump($statusses);
}
				
function getSitesetting($handle, $site) {

	$query = <<< EOM

SELECT * FROM keyvalue	
WHERE key = 'sitesetting_$site'

EOM;

	$results = $handle->query($query);
	$row = $results->fetchArray();

	return json_decode($row['value'], ture);
}
