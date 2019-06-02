import pytest
from nsweb.db import get_db


def test_index(client):
	response = client.get('/toukei')
	assert response.data == b'toukei index'


def test_daycount(client):
	response = client.get('/toukei/daycount?site=test')
	# TODO niascapeのテスト設定をtewtwebから突っ込めるようにする
	# TODO テストデータでアサート
	assert '日別投稿件数'in response.data.decode('utf-8')
