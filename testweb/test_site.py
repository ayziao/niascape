def test_timeline(client):
	response = client.get('/@test')
	assert 'タイムライン' in response.data.decode('utf-8')
	assert '2018-01-01' in response.data.decode('utf-8')
	assert 'title' in response.data.decode('utf-8')


def test_tag(client):
	response = client.get('/@test/?tag=tag')
	assert response.status_code == 200
	assert '#tag' in response.data.decode('utf-8')


def test_searchbody(client):
	response = client.get('/@test/?searchbody=body')
	assert response.status_code == 200
	assert 'body' in response.data.decode('utf-8')


def test_404(client):
	assert client.get('/@test/').status_code == 404
	assert client.get('/@test/12345678901234567890').status_code == 404
	assert client.get('/@test/20180101').status_code == 404
