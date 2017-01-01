<?php 
/*
 * 環境依存しなそうなの
 */

function vdump($obj){
  ob_start();
  var_dump($obj);
  $dump = ob_get_contents();
  ob_end_clean();
  return $dump;
}


/*
 * 環境どうにかするやつ
 */

function consoleLog($str){
	// fputs(fopen('php://stdout', 'w'), "\033[0;31m$str\n");
	fputs(fopen('php://stdout', 'w'), "\033[0m$str\n\033[0;31m");
}

function consoleErr($str){
	// fputs(fopen('php://stdout', 'w'), "\033[0;31m$str\033[0m\n");
	fputs(fopen('php://stdout', 'w'), "$str\n");
}

function shutdown()
{
	fputs(fopen('php://stdout', 'w'), "\033[0m");
}
fputs(fopen('php://stdout', 'w'), "\033[0;31m");
register_shutdown_function('shutdown');


/*
 * ニアスケイプ用？
 */
function loadIni(){
	return parse_ini_file(dirname(__FILE__)."/setting.ini");
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
