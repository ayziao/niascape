-- FIXME DB初期化をniascapeに作る

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

INSERT INTO "basedata"
VALUES
	('test', '12345678901234567890', '2018-01-01 00:00:00.000', 'title', ' #tag ', 'body');


--キーバリューストア PENDINGリレーショナルDBから取り除く？
CREATE TABLE `keyvalue`
(
	`key` TEXT NOT NULL
	,`value` TEXT NOT NULL

	,PRIMARY KEY(`key`)
);


--キュー PENDING ステータス(リトライ 中止とか) リトライ回数
CREATE TABLE `queue` (
	`serial_number`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`reservation_time`	TEXT NOT NULL,
	`queue_type`	TEXT NOT NULL,
	`content`	TEXT NOT NULL,
	`add_time`	TEXT NOT NULL
);


