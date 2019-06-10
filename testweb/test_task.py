import pytest
from nsweb.db import get_db


def test_index(client):
	response = client.get('/task')
	assert 'タスク' in response.data.decode('utf-8')
	assert '担当者なし' in response.data.decode('utf-8')


@pytest.mark.parametrize('path', (
		'/task/create',
		'/task/1/update',
))
def test_create_update_validate(client, path):
	# auth.login()
	response = client.post(path, data={'owner': '', 'title': '', 'tag': '', 'body': ''})
	assert b'Title is required.' in response.data


@pytest.mark.parametrize('path', (
		'/task/2/update',
		'/task/2/delete',
))
def test_exists_required(client, auth, path):
	auth.login()
	assert client.post(path).status_code == 404


def test_create(client, app):
	assert client.get('/task/create').status_code == 200
	client.post('/task/create', data={'owner': 'test', 'title': 'created', 'tag': '', 'body': ''})
	with app.app_context():
		db = get_db()
		count = db.execute('SELECT COUNT("連番") FROM task').fetchone()[0]
		assert count == 2


def test_update(client, app):
	# auth.login()
	assert client.get('/task/1/update').status_code == 200
	client.post('/task/1/update', data={'owner': 'test', 'title': 'updated', 'tag': '', 'body': ''})

	with app.app_context():
		db = get_db()
		task = db.execute('SELECT * FROM task WHERE "連番" = 1').fetchone()
		assert task['タスク名'] == 'updated'


def test_delete(client, auth, app):
	auth.login()
	response = client.post('/task/1/delete')
	assert response.headers['Location'] == 'http://localhost/task'

	with app.app_context():
		db = get_db()
		post = db.execute('SELECT * FROM post WHERE "連番" = 1').fetchone()
		assert post is None


def test_rateupdown(client, app):
	# auth.login()
	assert client.get('/task/1/rateup').status_code == 302

	with app.app_context():
		db = get_db()
		task = db.execute('SELECT * FROM task WHERE "連番" = 1').fetchone()
		assert task['重要度'] == 1

	assert client.get('/task/1/rateup').status_code == 302
	assert client.get('/task/1/rateup').status_code == 302
	assert client.get('/task/1/ratedown').status_code == 302

	with app.app_context():
		db = get_db()
		task = db.execute('SELECT * FROM task WHERE "連番" = 1').fetchone()
		assert task['重要度'] == 2


def test_done(client, app):
	# auth.login()
	assert client.get('/task/1/done').status_code == 302

	with app.app_context():
		db = get_db()
		task = db.execute('SELECT * FROM task WHERE "連番" = 1').fetchone()
		assert task['状態'] == '完'


def test_restore(client, app):
	# auth.login()
	assert client.get('/task/1/restore').status_code == 302

	with app.app_context():
		db = get_db()
		task = db.execute('SELECT * FROM task WHERE "連番" = 1').fetchone()
		assert task['状態'] == '未'
