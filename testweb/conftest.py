import os
import tempfile

import pytest
from nsweb import create_app
from nsweb.db import get_db, init_db
import niascape
from niascape.utility.database import get_db as ns_get_db
from configparser import ConfigParser

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
	_data_sql = f.read().decode('utf8')

with open(os.path.join(os.path.dirname(__file__), 'nstest.sql'), 'rb') as f:
	_ns_test_sql = f.read().decode('utf8')


@pytest.fixture
def app():
	db_fd, db_path = tempfile.mkstemp()
	ns_db_fd, ns_db_path = tempfile.mkstemp()

	app = create_app({
		'TESTING': True,
		'DATABASE': db_path,
	})

	with app.app_context():
		init_db()
		get_db().executescript(_data_sql)

	testconf = ConfigParser()
	testconf['database'] = {'dbms': 'sqlite', 'connect': ns_db_path}
	niascape.ini = testconf  # PENDING テスト用設定読むのどうにかしたい
	ns_get_db(niascape.ini['database']).executescript(_ns_test_sql)

	yield app

	os.close(db_fd)
	os.remove(db_path)

	os.close(ns_db_fd)
	os.remove(ns_db_path)


@pytest.fixture
def client(app):
	return app.test_client()


@pytest.fixture
def runner(app):
	return app.test_cli_runner()
