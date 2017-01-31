<?php
//フォローフォロアチェック
date_default_timezone_set('Asia/Tokyo');

require "../lib/twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

var_dump($argv);

$site = trim($argv[1]);
$userid = trim($argv[2]);


$ini_array = parse_ini_file(dirname(__FILE__) . "/../setting.ini");

$location = $ini_array['sqlite_file'];
$handle2 = new SQLite3($location);

$sitesetting = getSitesetting($handle2, $site);
$handle2->close();

$consumerKey = $sitesetting['twitter_main']['consumerKey'];
$consumerSecret = $sitesetting['twitter_main']['consumerSecret'];
$accessToken = $sitesetting['twitter_main']['accessToken'];
$accessTokenSecret = $sitesetting['twitter_main']['accessTokenSecret'];

$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

$following = $twitter->get("friends/ids", array("user_id" => $userid));
foreach ($following->ids as $value) {
	$followingids .= ',' . $value;
}
$followingids = substr($followingids, 1);

$followers = $twitter->get("followers/ids", array("user_id" => $userid));
foreach ($followers->ids as $value) {
	$followersids .= ',' . $value;
}
$followersids = substr($followersids, 1);

$handle = new SQLite3($ini_array['twitterdb']);
$query = 'UPDATE user SET following = 0 , followed = 0;';
$query .= 'UPDATE user SET following = 1 WHERE id IN (' . $followingids . ');';
$query .= 'UPDATE user SET followed = 1 WHERE id IN (' . $followersids . ');';
$handle->query($query);

function getSitesetting($handle, $site) {

	$query = <<< EOM

SELECT * FROM keyvalue	
WHERE key = 'sitesetting_$site'

EOM;

	$results = $handle->query($query);
	$row = $results->fetchArray();

	return json_decode($row['value'], ture);
}
