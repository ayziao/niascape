
def test_index(client):
	response = client.get('/task')
	assert 'タスク' in response.data.decode('utf-8')
	assert '未' in response.data.decode('utf-8')

