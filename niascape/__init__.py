"""
niascape パッケージ

"""
import os
import datetime
import configparser

import logging

logger = logging.getLogger(__name__)
logger.debug("import ニアスケイプ")

init_time = datetime.datetime.utcnow()  # type: datetime.datetime


def main(action_name: str = 'top', option: dict = None) -> str:
	"""
	ニアスケイプ 主処理

	:param action_name: アクション名
	:param option: オプションパラメータ辞書
	:return: 結果文字列
	"""
	from niascape import action

	# TODO アクション名受け取りじゃなくて位置引数リスト受け取りにする 1件目YYYYMMDD形式なら日サマリとか振り分け

	logger.debug("アクション: %s", action_name)
	logger.debug("オプション: %s", option)

	# FUTURE アクションのサブパッケージ化
	try:
		m = getattr(action, action_name)
	except AttributeError:
		logger.debug("AttributeError: %s", action_name)
		m = None

	if callable(m):
		return m(option)
	else:
		# PENDING 例外を投げる？警告を出す？ AttributeError SyntaxError ValueError SyntaxWarning ResourceWarning
		logger.info("アクションなし: %s", action_name)  # PENDING インフォかワーニングか設定で変えられるようにすべきか
		return 'No Action'


def _read_ini(file_name: str = 'config.ini') -> configparser.ConfigParser:
	# PENDING フルパス受け付けるか検討
	# PENDING config.ini が無い時 config.ini.sample を読むか検討
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	_ini = configparser.ConfigParser()
	_ini.read(path + '/' + file_name)
	return _ini


ini = _read_ini()  # PENDING __ini__での定義以外をやめるかどうか
