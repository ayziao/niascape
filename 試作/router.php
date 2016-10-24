<?php 

//ルーティング
function routing(){
	$path = substr($_SERVER["SCRIPT_NAME"],1);

	if (is_kobetu($path)) { //個別ページ判定	
		//個別ページ
		return require('kobetu.php');
	} else {
		return require($path . '.php');
	}

}

//個別ページ判定
function is_kobetu($path){
	return preg_match('/^[0-9]{20}?/', $path); //数字20文字だったら個別ページ
}

//ユーザ指定





return routing();
