"""
niascape パッケージ

"""
import os
from importlib import import_module
import datetime
import configparser

import logging

logger = logging.getLogger(__name__)
logger.debug("import ニアスケイプ")

init_time = datetime.datetime.utcnow()  # type: datetime.datetime


def main(action: str = 'top', option: dict = None) -> str:
	"""
	ニアスケイプ 主処理

	:param action: アクション名
	:param option: オプションパラメータ辞書
	:return: 結果文字列
	"""
	# TODO アクション名受け取りじゃなくて位置引数リスト受け取りにする 1件目YYYYMMDD形式なら日サマリとか振り分け

	logger.debug("アクション: %s", action)
	logger.debug("オプション: %s", option)

	actions = action.rsplit('.',1)
	if len(actions) > 1:
		usecase = _import_usecase('.'+actions[0])
		action = actions[1]
	else:
		usecase = _import_usecase('')

	try:
		m = getattr(usecase, action)
	except AttributeError:
		logger.debug("AttributeError: %s", action)
		m = None

	if callable(m):
		return m(option)
	else:
		# PENDING 例外を投げる？警告を出す？ AttributeError SyntaxError ValueError SyntaxWarning ResourceWarning
		logger.info("アクションなし: %s", action)  # PENDING インフォかワーニングか設定で変えられるようにすべきか
		return 'No Action'


def _import_usecase(m):
	logger.debug(m)
	module_name = 'niascape.usecase' + m
	module = import_module(module_name)
	logger.debug(module)

	return module


def _read_ini(file_name: str = 'config.ini') -> configparser.ConfigParser:
	# PENDING フルパス受け付けるか検討
	# PENDING config.ini が無い時 config.ini.sample を読むか検討
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	_ini = configparser.ConfigParser()
	_ini.read(path + '/' + file_name)
	return _ini


ini = _read_ini()  # PENDING __ini__での定義以外をやめるかどうか
