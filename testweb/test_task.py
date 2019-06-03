
def test_index(client):
	response = client.get('/task')
	assert response.data == b'task index'

