<?php
//ユーザー情報取得

date_default_timezone_set('Asia/Tokyo');

require "../lib/twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

var_dump($argv);

$site = trim($argv[1]);


$ini_array = parse_ini_file(dirname(__FILE__) . "/../setting.ini");
$location = $ini_array['twitterdb'];
$handle = new SQLite3($location);

$query = <<< EOM

select * from user 
WHERE lastdate < '2017-01-01 00:00:00'
AND checkdate < '2017-01-01 00:00:00'
ORDER BY id ASC LIMIT 100

EOM;
$results = $handle->query($query);

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	$ids .= ',' . $row['id'];
//	var_dump($row);
}
$ids = substr($ids, 1);

var_dump($ids);


$location = $ini_array['sqlite_file'];
$handle2 = new SQLite3($location);

$sitesetting = getSitesetting($handle2, $site);
$handle2->close();

$consumerKey = $sitesetting['twitter_main']['consumerKey'];
$consumerSecret = $sitesetting['twitter_main']['consumerSecret'];
$accessToken = $sitesetting['twitter_main']['accessToken'];
$accessTokenSecret = $sitesetting['twitter_main']['accessTokenSecret'];

$twitter = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

$result = $twitter->get("users/lookup", array("user_id" => $ids));

//var_dump($result);

$now = date('Y-m-d H:i:s');
$query = 'INSERT OR REPLACE INTO user VALUES ';
foreach ($result as $value) {
	$datetime = date('Y-m-d H:i:s', strtotime($value->status->created_at));
	$query .= "($value->id,'$value->screen_name','" . SQLite3::escapeString($value->name) . "','$datetime','$now'),";
}

$query = substr($query, 0, -1);
//var_dump($query);

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
