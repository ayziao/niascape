#!/usr/bin/env python3
"""
niascape.cli

コマンドラインインターフェース
"""
import os
import sys
from typing import List, Tuple, Dict, Union

import logging.config

logger = logging.getLogger(__name__)


def run(argv: List[str]) -> str:
	"""
	コマンドライン実行

	コマンドライン引数をパースしてニアスケイプメインに投げる

	:param argv: sys.argv
	:return: 結果文字列
	"""
	# PENDING 結果の出力をどのような形式にすべきか
	logger.debug("コマンドライン引数: %s", argv)

	arguments, option_dict, short_options = parse_argument_vector(argv)  # FUTURE ショートオプションの解析をどこでやるか検討

	if len(arguments) > 0:
		action = arguments[0]
	else:
		# FUTURE -help しろよメッセージ出す
		action = 'top'
	# FUTURE アクションなしだったら -help しろよメッセージ出しつつエラーコード終了

	import niascape
	return niascape.main(action, option_dict)  # PENDING オプション間違って unexpected keyword argument 出たらactionのhelp出す？


def parse_argument_vector(argv: List[str]) -> Tuple[List[str], Dict[str, Union[str, int, bool]], List[str]]:
	"""
	コマンドライン引数リストのパース

	:param argv: sys.argv
	:return: 位置引数, オプション引数辞書, ショートオプションリスト
	"""
	arguments = []  # type: List[str]
	option_dict = {}  # type: Dict[str, Union[str, int, bool]]
	short_options = []  # type: List[str]

	option_name = ''

	for argument in argv:
		if argument[0:2] == '--':
			if option_name != '':
				option_dict[option_name] = True
				option_name = ''
			if '=' in argument:
				key, val = argument[2:].split('=')
				option_dict[key] = _cast(val)
			else:
				option_name = argument[2:]
		elif argument[0] == '-':
			logger.debug(argument + ': short option')
			short_options.append(argument[1:])
		else:
			if option_name == '':
				arguments.append(argument)
			else:
				option_dict[option_name] = _cast(argument)
				option_name = ''

	if option_name != '':
		option_dict[option_name] = True

	return arguments[1:], option_dict, short_options  # argumentsの0を削ってwsgiと合わせる


def _cast(string: str) -> Union[str, int]:
	if string.isdigit():
		return int(string)
	# FUTURE 符号付き整数
	# FUTURE float
	# FUTURE bool
	# FUTURE カンマ区切りを配列にするか検討
	# FUTURE 他に変換すべき型はあるか検討
	return string


if __name__ == '__main__':  # pragma: no cover
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(path)  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	# import json ; logging.config.dictConfig(json.load(open(path + '/tests/logger_config.json', 'r'))) ; logger = logging.getLogger()

	# sys.argv.extend("daycount --site test --tag=#test --search_body test".split())
	# sys.argv.extend("timeline --site test".split())

	print(run(sys.argv))
