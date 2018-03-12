"""
niascape パッケージ

"""
import os
import datetime
import configparser

init_time = datetime.datetime.utcnow()

from niascape.__main__ import run  # PENDING __ini__で定義すべきか
from niascape.cli import cli
from niascape.wsgiapplication import application


def _readini(file_name='config.ini'):
	# PENDING フルパス受け付けるか検討
	# PENDING config.ini が無い時 config.ini.sample を読むか検討
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	_ini = configparser.ConfigParser()
	_ini.read(path + '/' + file_name)
	return _ini


ini = _readini()  # PENDING __ini__での定義以外をやめるかどうか
