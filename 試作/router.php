<?php 
//ルーティング

$path = substr($_SERVER["SCRIPT_NAME"],1);

if (preg_match('/^[0-9]{20}?/', $path)) {	//数字20文字だったら個別ページ
	//個別ページ
	return require('kobetu.php');
} else {
	return require($path . '.php');
}

