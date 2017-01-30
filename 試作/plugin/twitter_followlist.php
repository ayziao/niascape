<?php
//フォローリスト

date_default_timezone_set('Asia/Tokyo');
header('Content-Type: text/html; charset=UTF-8');


$ini_array = parse_ini_file(dirname(__FILE__) . "/../setting.ini");
$location = $ini_array['twitterdb'];
$handle = new SQLite3($location);

$query = <<< EOM

select * from user WHERE following = 1 AND followed = 1

EOM;
$results = $handle->query($query);

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	$aaa .= '<tr><td>'.$row['id'] .'</td><td>'.$row['screen_name'] .'</td><td>'.$row['name'];
	
	if($row['following'] == 1 &&$row['followed'] == 1){
		$aaa .= '</td><td>相互';
	} elseif ($row['following'] == 1 &&$row['followed'] == 0) {
		$aaa .= '</td><td>片思い';
	} elseif ($row['following'] == 0 &&$row['followed'] == 1) {
		$aaa .= '</td><td>片思われ';
	} else {
		$aaa .= '</td><td>無関係';
	}
//	  'lastdate' => '2017-01-28 23:33:18',
//  'checkdate' => '2017-01-28 23:33:18'	
	$aaa .= '</td></tr>';
}

$query = <<< EOM

select * from user WHERE following = 1 AND followed = 0 

EOM;
$results = $handle->query($query);

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	$aaa .= '<tr><td>'.$row['id'] .'</td><td>'.$row['screen_name'] .'</td><td>'.$row['name'];
	
	if($row['following'] == 1 &&$row['followed'] == 1){
		$aaa .= '</td><td>相互';
	} elseif ($row['following'] == 1 &&$row['followed'] == 0) {
		$aaa .= '</td><td>片思い';
	} elseif ($row['following'] == 0 &&$row['followed'] == 1) {
		$aaa .= '</td><td>片思われ';
	} else {
		$aaa .= '</td><td>無関係';
	}
//	  'lastdate' => '2017-01-28 23:33:18',
//  'checkdate' => '2017-01-28 23:33:18'	
	$aaa .= '</td></tr>';
}


$query = <<< EOM

select * from user WHERE following = 0 AND followed = 1

EOM;
$results = $handle->query($query);

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	$aaa .= '<tr><td>'.$row['id'] .'</td><td>'.$row['screen_name'] .'</td><td>'.$row['name'];
	
	if($row['following'] == 1 &&$row['followed'] == 1){
		$aaa .= '</td><td>相互';
	} elseif ($row['following'] == 1 &&$row['followed'] == 0) {
		$aaa .= '</td><td>片思い';
	} elseif ($row['following'] == 0 &&$row['followed'] == 1) {
		$aaa .= '</td><td>片思われ';
	} else {
		$aaa .= '</td><td>無関係';
	}
//	  'lastdate' => '2017-01-28 23:33:18',
//  'checkdate' => '2017-01-28 23:33:18'	
	$aaa .= '</td></tr>';
}

$query = <<< EOM

select * from user WHERE following = 0 AND followed = 0 

EOM;
$results = $handle->query($query);

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
	$aaa .= '<tr><td>'.$row['id'] .'</td><td>'.$row['screen_name'] .'</td><td>'.$row['name'];
	
	if($row['following'] == 1 &&$row['followed'] == 1){
		$aaa .= '</td><td>相互';
	} elseif ($row['following'] == 1 &&$row['followed'] == 0) {
		$aaa .= '</td><td>片思い';
	} elseif ($row['following'] == 0 &&$row['followed'] == 1) {
		$aaa .= '</td><td>片思われ';
	} else {
		$aaa .= '</td><td>無関係';
	}
//	  'lastdate' => '2017-01-28 23:33:18',
//  'checkdate' => '2017-01-28 23:33:18'	
	$aaa .= '</td></tr>';
}

?>
<html>
	<head>
		<title>フォローリスト</title>
	</head>

	<body>
		<h1>フォローリスト</h1>
		
		<table>
			<?= $aaa ?>
		</table>

	</body>
</html>