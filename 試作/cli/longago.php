<?php
//長いこと更新がない

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

EOM;
$results = $handle->query($query);

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	$link .= '<a href="https://twitter.com/' . $row['screen_name'] . '">' . $row['screen_name'].' '.$row['name'] . "  </a><br>\n";
	$count++;
}


ob_start();
?>
<html>
	<head>
		<title>長いこと更新がない</title>
	</head>
	<body>
		<h1>長いこと更新がない <?= $count ?></h1>
		<?= $link ?>
	</body>
</html>
<?php
$dump = ob_get_contents();
ob_end_clean();

file_put_contents($argv[2].'ever.html', $dump);
