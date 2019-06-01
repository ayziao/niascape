import pytest
from nsweb.db import get_db


def test_index(client):
	response = client.get('/toukei')
	assert response.data == b'toukei index'


def test_daycount(client):
	response = client.get('/toukei/daycount')
	# TODO niascapeのテスト設定をtewtwebから突っ込めるようにする
	assert '日別投稿件数'in response.data.decode('utf-8')