<?php 

function consoleLog($str){
	// fputs(fopen('php://stdout', 'w'), "\033[0;31m$str\n");
	fputs(fopen('php://stdout', 'w'), "\033[0m$str\n\033[0;31m");
}

function consoleErr($str){
	// fputs(fopen('php://stdout', 'w'), "\033[0;31m$str\033[0m\n");
	fputs(fopen('php://stdout', 'w'), "$str\n");
}

function loadIni(){

	return parse_ini_file(dirname(__FILE__)."/setting.ini");
}

function vdump($obj){
  ob_start();
  var_dump($obj);
  $dump = ob_get_contents();
  ob_end_clean();
  return $dump;
}






function shutdown()
{
	fputs(fopen('php://stdout', 'w'), "\033[0m");
}
fputs(fopen('php://stdout', 'w'), "\033[0;31m");
register_shutdown_function('shutdown');

