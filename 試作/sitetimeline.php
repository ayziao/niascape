<?php
/*
 * サイトタイムライン 
 */

function getSitesetting($handle, $site) {

	$query = <<< EOM

SELECT * FROM keyvalue	
WHERE key = 'sitesetting_$site'

EOM;

	$results = $handle->query($query);
	$row = $results->fetchArray();

	return json_decode($row['value'], ture);
}

header('Content-Type: text/html; charset=UTF-8');

$ini_array = parse_ini_file(dirname(__FILE__) . "/setting.ini");
$location = $ini_array['sqlite_file'];
$handle = new SQLite3($location);


if (strpos($_SERVER['HTTP_HOST'], $ini_array['host']) > 0) {
	$site = explode('.' . $ini_array['host'], $_SERVER['HTTP_HOST'])[0];
} else {
	$site = explode("/", substr($_SERVER["SCRIPT_NAME"], 2))[0];
}
if ($_GET['tagiji']) {
	$tagiji = 'checked="checked"';
}

$sitesetting = getSitesetting($handle, $site);

$query = <<< EOM

SELECT * FROM basedata
WHERE site = '$site'
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
	$day2 = substr($row['datetime'], 0, 10);
	if ($day != $day2) {
		if ($day != '') {
			$content .= "\n\t\t\t</div>";
		}
		$content .= "\n\t\t\t" . '<h5><a href="./' . str_replace('-', '', $day2) . '">' . $day2 . '</a></h5> ' . "\n\t\t\t" . '<div class="lines">';
		$day = $day2;
	}

	$tagstr = '';
	$tags = explode(' ', trim($row['tags']));
	foreach ($tags as $value) {
		if (strpos($value, '#') === 0) {
			$tag = substr($value, 1);
			$tagstr .= ' <a href="./?tag=' . $tag . '">' . $tag . '</a>';
		}
	}

	$content .= "\n\t\t\t\t" . '<div class="line"><span class="time"><a href="./' . $row['identifier'] . '">' . substr($row['datetime'], -8) . '</a></span>&thinsp;'
					. str_replace("\n", '<br/>', str_replace("\r\n", '<br/>', $row['body'])) . $tagstr . '</div>';
}
$content .= "\n\t\t\t</div>";
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title>タイムライン <?= $site ?></title>
		<link rel="icon" type="image/png" href="./favicon.png">
		<link rel="stylesheet" type="text/css" href="/common.css">
		<link rel="stylesheet" type="text/css" href="./css.css">
		<style type="text/css">
			.table { display: table; width: 100%; }
			.cell { display: table-cell;}
		</style>
	</head>

	<body>
		<form action="./" method="POST" enctype="multipart/form-data" onsubmit="return submit();">
			<div class="table">
				<h1 class="cell"><a href="./"><?= $site ?></a>　</h1>
				<div class="cell">
					<input class="file" type="file" name="file" accept="image/*">
					<input type="checkbox" name="tagiji" value="tagiji" <?= $tagiji ?>>タグ維持
					<input id="tag" class="text" type="text" name="tags" onKeyup="showmojilen();" value="<?= $_GET['ijitag'] ?>" placeholder="タグ">
				</div>
			</div>
			<div class="table">
				<div class="textarea cell" style="width: 100%;">
					<textarea id="box" name="body" onKeyup="showmojilen();"><?= $_GET['form'] ?></textarea>
				</div>
				<div class="cell" style="vertical-align: middle;">
					<input id="btn" class="submitbutton" type="button" name="post" value="post" onclick="return submit();">
				</div>
			</div>

			<input type="text" name="post" style="display:none;">
			<input type="hidden" name="site" value="<?= $site ?>">

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

				var charcount = function (str) {
				  len = 0;
				  str = escape(str);
				  for (i=0;i<str.length;i++,len++) {
					if (str.charAt(i) == "%") {
					  if (str.charAt(++i) == "u") {
						i += 3;
						len++;
					  }
					  i++;
					}
				  }
				  return len;
				}
				
				var counter = function(str,seq){
					return str.split(seq).length - 1;
				}

				function showmojilen() {
					var taglen = charcount(tag.value.trim());
					if (taglen > 0) {
						taglen += 2 + counter(tag.value.trim(),' ') * 2;
					}
					var bodylen = charcount(textbox.value.trim());
					var strlen = bodylen + taglen;
					if (sbmit === false) {
						if (bodylen === 0 || strlen > 280) {
							submitButton.disabled = true;
							submitButton.value = 'post';
						} else {
							submitButton.disabled = false;
							submitButton.value = strlen;
						}
					}
				}

				function submit() {
					if (sbmit === true) {
						alert('投稿無効');
						return false;
					}
					;

					sbmit = true;
					submitButton.disabled = true;
					submitButton.value = '送信中';

					return true;
				}

				setInterval("showmojilen()", 1000);

			</script>

		</form>

		<div id="etc"><?= $sitesetting['siteinsert'] ?></div>

		<div>

			<?= $content ?>

		</div>

		<div><a href="./">top</a></div>
		<form action="./" method="GET">
			<input id="search" class="text" type="text" name="searchbody">
			<input id="btn" class="submitbutton" type="submit" name="submit" value="検索">
		</form>
	</body>
</html>
