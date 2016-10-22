<?php 
//<pre>
//var_dump($_GET);
//var_dump($_SERVER["SCRIPT_NAME"]);
//phpinfo();

$path = substr($_SERVER["SCRIPT_NAME"],1);


return require($path . '.php');

