<?php 
//ini_set( 'display_errors', 0 ); //ビルトインサーバでのエラーログの出力先がよくわからん		
//ini_set( 'error_log', 1 ); //ビルトインサーバでのエラーログの出力先がよくわからん		
//error_log('hoge');


//ルーティング
function routing(){
	$path = $_SERVER["SCRIPT_NAME"];

	//TODO トップページ判定

	if (is_kobetupage($path)) { //個別ページ判定	
		return require('kobetu.php');
	} elseif(is_daysummary($path)) {	//日サマリー判定	
		return require('daysummary.php');
	} elseif(is_sitetimeline($path)) {	//サイトタイムライン判定
		return require('sitetimeline.php');
	} else {
		return @include(substr($path,1) . '.php');	//PENDING 画面じゃなくてコンソールにエラーが吐ければ@取りたい
	}
}

//個別ページ判定
function is_kobetupage($path){
	//PENDING サイトチェック入れるか	
	return preg_match('/\/[0-9]{20}$/', $path); //末尾が数字20文字だったら個別ページ
}

//日サマリー判定
function is_daysummary($path){
	return preg_match('/\/[0-9]{8}$/', $path);	//末尾が数字8文字だったら日サマリー
}

//サイトタイムライン判定
function is_sitetimeline($path){
	//TODO バーチャルホスト
	return preg_match('/^\/@\w/', $path);	//1文字目が＠ならユーザページ
}



return routing();
