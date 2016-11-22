--ベースデータ
CREATE TABLE "basedata" 
(
	`site` TEXT
	,`identifier` TEXT
	,`datetime` TEXT
	,`title` TEXT
	,`tags` TEXT
	,`body` TEXT

	,PRIMARY KEY(`site`,`identifier`)
);

--キーバリューストア PENDINGリレーショナルDBから取り除く？
CREATE TABLE `keyvalue` 
(
	`key` TEXT NOT NULL
	,`value` TEXT NOT NULL

	,PRIMARY KEY(`key`)
);

