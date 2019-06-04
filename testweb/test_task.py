from nsweb.db import get_db

def test_index(client):
	response = client.get('/task')
	assert 'タスク' in response.data.decode('utf-8')
	assert '未' in response.data.decode('utf-8')


def test_create(client,app):
	assert client.get('/task/create').status_code == 200
	client.post('/task/create', data={'owner':'test','title': 'created', 'tag': '', 'body': ''})
	with app.app_context():
		db = get_db()
		count = db.execute('SELECT COUNT("連番") FROM task').fetchone()[0]
		assert count == 2
