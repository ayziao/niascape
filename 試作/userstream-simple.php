<?php
date_default_timezone_set('Asia/Tokyo');

require_once('./lib/UserstreamPhirehose.php');

$ini_array = parse_ini_file("setting.ini");
$handle    = new SQLite3($ini_array['sqlite_file']); 
$sitesetting = getSitesetting($handle,$ini_array['default_site']);
$consumerKey = $sitesetting['twitter_main']['consumerKey'];
$consumerSecret = $sitesetting['twitter_main']['consumerSecret'];
$accessToken = $sitesetting['twitter_main']['accessToken'];
$accessTokenSecret = $sitesetting['twitter_main']['accessTokenSecret'];

/**
 * Barebones example of using UserstreamPhirehose.
 */
class MyUserConsumer extends UserstreamPhirehose 
{
  /**
   * First response looks like this:
   *    $data=array('friends'=>array(123,2334,9876));
   *
   * Each tweet of your friends looks like:
   *   [id] => 1011234124121
   *   [text] =>  (the tweet)
   *   [user] => array( the user who tweeted )
   *   [entities] => array ( urls, etc. )
   *
   * Every 30 seconds we get the keep-alive message, where $status is empty.
   *
   * When the user adds a friend we get one of these:
   *    [event] => follow
   *    [source] => Array(   my user   )
   *    [created_at] => Tue May 24 13:02:25 +0000 2011
   *    [target] => Array  (the user now being followed)
   *
   * @param string $status
   */
  public function enqueueStatus($status)
  {
    /*
     * In this simple example, we will just display to STDOUT rather than enqueue.
     * NOTE: You should NOT be processing tweets at this point in a real application, instead they
     *  should be being enqueued and processed asyncronously from the collection process. 
     */
    // $data = json_decode($status, true);
    // echo date("Y-m-d H:i:s (").strlen($status)."):".print_r($data,true)."\n";

    file_put_contents('tw_'.date("Ymd").'.txt', $status."\n" , FILE_APPEND);
  }

}

// The OAuth credentials you received when registering your app at Twitter
define("TWITTER_CONSUMER_KEY", $consumerKey);
define("TWITTER_CONSUMER_SECRET", $consumerSecret);


// The OAuth data for the twitter account
define("OAUTH_TOKEN",$accessToken  );
define("OAUTH_SECRET", $accessTokenSecret);



// Start streaming
$sc = new MyUserConsumer(OAUTH_TOKEN, OAUTH_SECRET);
$sc->consume();






function getSitesetting($handle,$site){

  $query = <<< EOM

SELECT * FROM keyvalue  
WHERE key = 'sitesetting_$site'

EOM;

  $results = $handle->query($query); 
  $row = $results->fetchArray();

  return json_decode($row['value'],ture);
}

