<?php 
date_default_timezone_set('Asia/Tokyo');

ini_set('display_errors',0);
ini_set('log_errors','On');
ini_set('error_log', 'php://stderr');

require('common.php');


//ルーティング
function routing(){
	$path = $_SERVER["SCRIPT_NAME"];

	if($_SERVER["REQUEST_METHOD"] == "POST"){
		if (array_key_exists('post',$_POST)){
			return require('post.php');
		} elseif (array_key_exists('tagUpdate',$_POST)){
			return require('tagUpdate.php');
		}
	}
	//TODO トップページ判定

	if (is_kobetupage($path)) {        //個別ページ判定	
		return require('kobetu.php');
	} elseif(is_daysummary($path)) {   //日サマリー判定	
		return require('daysummary.php');
	} elseif(is_tagtimeline($path)) {  //タグタイムライン判定
		return require('tagtimeline.php');
	} elseif(is_search($path)) {       //本文検索
		return require('search.php');
	} elseif(is_sitetimeline($path)) { //サイトタイムライン判定
		return require('sitetimeline.php');
	} elseif(is_site_static($path)) { //サイト別静的ファイル

		$ini_array = loadIni();
		content_type($path);

		if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
			$path = explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0] . $path;
		} else {
			$path = substr($path, 2);
		}

		readfile($ini_array['site_static'].$path);
		consoleLog($path);
		return;

	} elseif(isset($_GET['kanri'])) {
		return include('kanri/'.$_GET['kanri'] . '.php');
	} else {
		return @include(substr($path,1) . '.php');	//PENDING 画面じゃなくてコンソールにエラーが吐ければ@取りたい
	}
}

//個別ページ判定
function is_kobetupage($path){
	//PENDING サイトチェック入れるか	
	return preg_match('#/[0-9]{20}$#', $path); //末尾が数字20文字だったら個別ページ
}

//日サマリー判定
function is_daysummary($path){
	return preg_match('#/[0-9]{8}$#', $path);	//末尾が数字8文字だったら日サマリー
}

//タグタイムライン判定
function is_tagtimeline($path){
	return (is_sitetimeline($path) and array_key_exists('tag', $_GET));
}

//本文検索
function is_search($path){
	return (is_sitetimeline($path) and array_key_exists('searchbody', $_GET));
}

//サイト別静的ファイル
function is_site_static($path){
	$ini_array = loadIni(); //parse_ini_file(__FILE__."/setting.ini");

	if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
		$path = explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0] . $path;
	} else {
		$path = substr($path, 2);
	}
	return (!is_dir($ini_array['site_static'].$path) and is_readable($ini_array['site_static'].$path));
}

//サイトタイムライン判定
function is_sitetimeline($path){
	//TODO バーチャルホスト

	if (strpos($path, '.')){
		return false;
	}
	$ini_array = loadIni(); //parse_ini_file(__FILE__."/setting.ini");
	if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
		return true;
	}
	return preg_match('#^/@\w#', $path);	//1文字目が＠ならユーザページ
}

function content_type($path){
	$ini_array = loadIni(); //parse_ini_file(__FILE__."/setting.ini");		
	$kakutyousi = end(explode('.', $path));
	$arr = ['css' => 'Content-Type: text/css; charset=UTF-8'];
	if (array_key_exists($kakutyousi, $arr)){
		header($arr[$kakutyousi]);
	} else {

		if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0){
			$path = explode('.'.$ini_array['host'],$_SERVER['HTTP_HOST'])[0] . $path;
		} else {
			$path = substr($path, 2);
		}

		header('Content-Type: ' . mime_content_type($ini_array['site_static'].$path));
	}
}

// $stdout = fopen('php://stdout', 'w');
// fputs($stdout, "STDOUT\n");
// $stderr = fopen('php://stderr', 'w');
// fputs($stderr, "Error\n");
return routing();

