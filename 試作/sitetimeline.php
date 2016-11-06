<?php 
header('Content-Type: text/html; charset=UTF-8');

//サイトタイムライン

$ini_array = parse_ini_file("setting.ini");
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location); 

$user = explode("/", substr($_SERVER["SCRIPT_NAME"],2))[0];

$query = <<< EOM

SELECT * FROM basedata
WHERE user = '$user'
AND tags NOT LIKE '% gyazo_posted %'
ORDER BY identifier DESC LIMIT 200

EOM;

$results = $handle->query($query); 
//$raw = $results->fetchArray();

//print('<pre>');
//var_dump($query);

$day = '';

//TODO 時間区切りを入れる

while ($row = $results->fetchArray()) {
	$day2 = substr($row['datetime'], 0,10);
	if($day != $day2){
		if($day != ''){
			$content .= "\n\t\t\t</div>";
		}
		$content .= "\n\t\t\t". '<h5><a href="./'. str_replace('-', '', $day2).'">'.$day2.'</a></h5> '. "\n\t\t\t". '<div class="lines">';
		$day = $day2;
	}

	$tagstr = '';
	$tags = explode(' ',trim($row['tags']));
	foreach ($tags as  $value) {
		if(strpos($value , '#') === 0){
			$tag = substr($value, 1);
			$tagstr .= ' <a href="./?tag=' . $tag .'">' . $tag .'</a>';
		}
	}

	$content .= "\n\t\t\t\t". '<div class="line"><span class="time"><a href="./'.$row['identifier'].'">'.substr($row['datetime'], -8).'</a></span>&thinsp;'.str_replace("\n", '<br>', $row['body']).$tagstr.'</div>';
}
$content .= "\n\t\t\t</div>";

?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title>タイムライン <?=$user?></title>
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="/css.css">
	</head>

	<body>
		<h1><?=$user?></h1>

		<form action="./" method="POST" enctype="multipart/form-data" onsubmit="return submit();">
			<div class="textarea">
				<textarea id="box" name="body" onKeyup="showmojilen();"><?=$_GET['form']?></textarea>
			</div>
			tag<input id="tag" class="text" type="text" name="tags" onKeyup="showmojilen();">
			<input id="btn" class="submitbutton" type="submit" name="submit" value="post" onclick="return submit();">
			<input class="file" type="file" name="file" accept="image/*">
			<input type="hidden" name="user" value="test">
			
			<script type="text/javascript">
				var key = "none";
				var sbmit = false;
				var textbox = document.getElementById('box');
				var tag = document.getElementById('tag');
				var submitButton = document.getElementById('btn');

				submitButton.disabled = true;

				textbox.addEventListener('keydown',
						function (e) {
							key = e.which;
							if (sbmit === false && e.metaKey && e.which == 13) {
								submitButton.click();
								submit();
							}
						},
						false
						);

				function showmojilen() {
					var taglen = tag.value.trim().length;
					if (taglen > 0) {
						taglen += 2;
					}
					var bodylen = textbox.value.trim().length;
					var strlen = bodylen + taglen;
					if (sbmit === false){
						if (bodylen === 0 || strlen > 140) {
							submitButton.disabled = true;
							submitButton.value = 'post';
						} else {
							submitButton.disabled = false;
							submitButton.value = strlen;
						}
					}
				}
				
				function submit(){
					if(sbmit === true){ 
						alert('投稿無効');
						return false; 
					};
					
					sbmit = true;
					submitButton.disabled = true;
					submitButton.value = '送信中';
					
					return true;
				}

				setInterval("showmojilen()", 1000);

			</script>

		</form>

		<div id="etc"></div>
		
		<div>

			<?=$content?>

		</div>

		<div><a href="./">top</a></div>
		<form action="./" method="GET">
			<input id="search" class="text" type="text" name="searchbody">
			<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
		</form>
	</body>
</html>
