import pytest
from nsweb.db import get_db


def test_index(client):
	response = client.get('/toukei')
	assert response.data == b'toukei index'


def test_daycount(client):
	response = client.get('/toukei/daycount')
	assert b'site' in response.data
