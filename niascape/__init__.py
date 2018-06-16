"""
niascape パッケージ

"""
import os
import datetime
import configparser

import logging

_logger = logging.getLogger(__name__)
_logger.log(5, "import ニアスケイプ")

init_time = datetime.datetime.utcnow()  # type: datetime.datetime


def main(action: str = 'top', option: dict = None) -> str:
	"""
	ニアスケイプ 主処理

	:param action: アクション名
	:param option: オプションパラメータ辞書
	:return: 結果文字列
	"""
	# PENDING アクション名受け取りじゃなくて位置引数リスト受け取りにする？ 1件目YYYYMMDD形式なら日サマリとか振り分け？

	_logger.log(10, "アクション: %s", action)
	_logger.log(5, "オプション: %s", option)

	from niascape import utility

	m = utility.dynamic_get_method('niascape.usecase', action)

	if m is None:  # PENDING 例外を投げる？警告を出す？ AttributeError SyntaxError ValueError SyntaxWarning ResourceWarning
		_logger.info("アクションなし: %s", action)  # PENDING インフォかワーニングか設定で変えられるようにすべきか
		return 'No Action'

	return m(option)


def _read_ini(file_name: str = 'config.ini') -> configparser.ConfigParser:
	# PENDING フルパス受け付けるか検討
	# PENDING config.ini が無い時 config.ini.sample を読むか検討
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	_ini = configparser.ConfigParser()
	_ini.read(path + '/' + file_name)
	return _ini


ini = _read_ini()  # PENDING __ini__での定義以外をやめるかどうか
