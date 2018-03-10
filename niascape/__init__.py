"""
niascape パッケージ

"""
import os
import datetime
import configparser

from niascape.__main__ import run
from niascape.wsgiapplication import application

init_time = datetime.datetime.utcnow()


def _readini(file_name='config.ini'):
	# PENDING フルパス受け付けるか検討
	# PENDING config.ini が無い時 config.ini.sample を読むか検討
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	ini = configparser.ConfigParser()
	ini.read(path + '/' + file_name)
	return ini


ini = _readini()
