<?php 
date_default_timezone_set('Asia/Tokyo');
// phpinfo();

require('common.php');

//Twitterタイムライン取得
require "twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;


$ini_array = parse_ini_file("setting.ini");
$handle    = new SQLite3($ini_array['sqlite_file']); 
$sitesetting = getSitesetting($handle,$ini_array['default_site']);
$consumerKey = $sitesetting['twitter_main']['consumerKey'];
$consumerSecret = $sitesetting['twitter_main']['consumerSecret'];
$accessToken = $sitesetting['twitter_main']['accessToken'];
$accessTokenSecret = $sitesetting['twitter_main']['accessTokenSecret'];
$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

$parms = array('count' => '5');
$res = $twitter->get('statuses/user_timeline', $parms);

//echo '<pre>';
var_dump($res);

