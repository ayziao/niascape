"""
niascape パッケージ

"""
import os
import datetime
import configparser
import json

import logging

_logger = logging.getLogger(__name__)
_logger.log(5, "import ニアスケイプ")

init_time = datetime.datetime.utcnow()  # type: datetime.datetime


def main(arguments: list, option: dict = None) -> str:
	"""
	ニアスケイプ 主処理

	:param arguments: アクション名
	:param option: オプションパラメータ辞書
	:return: 結果文字列
	"""
	# PENDING 1件目YYYYMMDD形式なら日サマリとか振り分け？

	_logger.log(10, "arg: %s", arguments)
	_logger.log(5, "オプション: %s", option)

	from niascape import utility
	from niascape.utility.json import AsdictSupportJSONEncoder

	if len(arguments) > 0:
		action = arguments[0]
	else:
		# FUTURE アクションなし例外ありモード(CLIなど)でアクションなしだったら例外投げる
		action = 'top'

	m = utility.dynamic_get_method('niascape.usecase', action)

	if m is None:  # PENDING 例外を投げる？警告を出す？ AttributeError SyntaxError ValueError SyntaxWarning ResourceWarning
		_logger.info("アクションなし: %s", action)  # PENDING インフォかワーニングか設定で変えられるようにすべきか
		return 'No Action'

	if option is not None and 'media_type' in option:
		if option['media_type'] != 'json':
			return 'media err'
		media_type = option.pop('media_type')

	# FUTURE 表示形式変換 view的なもの作る

	return json.dumps(m(option), cls=AsdictSupportJSONEncoder)


def _read_ini(file_name: str = 'config.ini') -> configparser.ConfigParser:
	# PENDING フルパス受け付けるか検討
	# PENDING config.ini が無い時 config.ini.sample を読むか検討
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	_ini = configparser.ConfigParser()
	_ini.read(path + '/' + file_name)
	return _ini


ini = _read_ini()  # PENDING __ini__での定義以外をやめるかどうか
