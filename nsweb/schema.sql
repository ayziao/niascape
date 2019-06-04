DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS task;


CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE post(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	title TEXT NOT NULL,
	body TEXT NOT NULL,
	FOREIGN KEY(author_id) REFERENCES user(id)
);

CREATE TABLE "task"(
	"連番" INTEGER PRIMARY KEY AUTOINCREMENT,
	"状態" TEXT NOT NULL DEFAULT '未',
	"所有者" TEXT NOT NULL,
	"タスク名" TEXT NOT NULL,
	"重要度" INTEGER NOT NULL DEFAULT 0,
	"予定日" TEXT NOT NULL DEFAULT '9999-12-31',
	"タグ" TEXT NOT NULL,
	"備考" TEXT NOT NULL,
	"親タスク" INTEGER NOT NULL DEFAULT 0,
	"追加日時" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"変更日時" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"完了日時" TEXT NOT NULL DEFAULT ''
);
