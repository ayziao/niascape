<?php
date_default_timezone_set('Asia/Tokyo');

ini_set('display_errors', 0);
ini_set('log_errors', 'On');
ini_set('error_log', 'php://stderr');

//require('common.php');

function loadIni() {
	return parse_ini_file(dirname(__FILE__) . "/setting.ini");
}

/*
 * 環境どうにかするやつ
 */

function consoleLog($str) {
	// fputs(fopen('php://stdout', 'w'), "\033[0;31m$str\n");
	fputs(fopen('php://stdout', 'w'), "\033[0m$str\n\033[0;31m"); //エラーの色つけのために黒にしてからなんか出して赤にしてる
}

function consoleErr($str) {
	// fputs(fopen('php://stdout', 'w'), "\033[0;31m$str\033[0m\n");
	fputs(fopen('php://stdout', 'w'), "$str\n");
}

function shutdown() {
	fputs(fopen('php://stdout', 'w'), "\033[0m"); //終了時色を戻す
}

fputs(fopen('php://stdout', 'w'), "\033[0;31m");
register_shutdown_function('shutdown');

//個別ページ判定
function is_kobetupage($path) {
	//PENDING サイトチェック入れるか	
	return preg_match('#/[0-9]{20}$#', $path); //末尾が数字20文字だったら個別ページ
}

//日サマリー判定
function is_daysummary($path) {
	return preg_match('#/[0-9]{8}$#', $path); //末尾が数字8文字だったら日サマリー
}

//タグタイムライン判定
function is_tagtimeline($path) {
	return (is_sitetimeline($path) and array_key_exists('tag', $_GET));
}

//本文検索
function is_search($path) {
	return (is_sitetimeline($path) and array_key_exists('searchbody', $_GET));
}

//サイト別静的ファイル
function is_site_static($path) {
	$ini_array = loadIni();

	if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
		$path = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0] . $path;
	} else {
		$path = substr($path, 2);
	}
	return ( ! is_dir($ini_array['site_static'] . $path) and is_readable($ini_array['site_static'] . $path));
}

//サイトタイムライン判定
function is_sitetimeline($path) {
	//TODO バーチャルホスト

	if (strpos($path, '.')) {
		return false;
	}
	$ini_array = loadIni();
	if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
		return true;
	}
	return preg_match('#^/@\w#', $path); //1文字目が＠ならユーザページ
}

function content_type($path) {
	$ini_array = loadIni();
	$kakutyousi = end(explode('.', $path));
	$arr = ['css' => 'Content-Type: text/css; charset=UTF-8'];
	if (array_key_exists($kakutyousi, $arr)) {
		header($arr[$kakutyousi]);
	} else {

		if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
			$path = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0] . $path;
		} else {
			$path = substr($path, 2);
		}

		header('Content-Type: ' . mime_content_type($ini_array['site_static'] . $path));
	}
}

$path = $_SERVER["SCRIPT_NAME"];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	if (array_key_exists('post', $_POST)) {
		return require('post.php');
	} elseif (array_key_exists('tagUpdate', $_POST)) {
		return require('tagUpdate.php');
	}
}
//TODO トップページ判定

if (is_kobetupage($path)) { //個別ページ判定	
	return require('kobetu.php');
} elseif (is_daysummary($path)) { //日サマリー判定	
	return require('daysummary.php');
} elseif (is_tagtimeline($path)) { //タグタイムライン判定
	return require('tagtimeline.php');
} elseif (is_search($path)) { //本文検索
	return require('search.php');
} elseif (is_sitetimeline($path)) { //サイトタイムライン判定
	return require('sitetimeline.php');
} elseif (is_site_static($path)) { //サイト別静的ファイル
	$ini_array = loadIni();
	content_type($path);

	if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
		$path = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0] . $path;
	} else {
		$path = substr($path, 2);
	}

	readfile($ini_array['site_static'] . $path);
	consoleLog($path);
	return;
} elseif (isset($_GET['kanri'])) { //管理系
	return include('kanri/' . $_GET['kanri'] . '.php');
} elseif (isset($_GET['plugin'])) { //プラグイン
	return include('plugin/' . $_GET['plugin'] . '.php');
} if(file_exists(substr($path, 1) . '.php')) {
	return include(substr($path, 1) . '.php');
}

return false;
