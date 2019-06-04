from nsweb.db import get_db


def test_index(client):
	response = client.get('/task')
	assert 'タスク' in response.data.decode('utf-8')
	assert '未' in response.data.decode('utf-8')


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
		post = db.execute('SELECT * FROM task WHERE "連番" = 1').fetchone()
		assert post['タスク名'] == 'updated'
