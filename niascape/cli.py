#!/usr/bin/env python3
"""
コマンドラインインターフェース
"""
import os
import sys
from typing import List, Tuple, Dict, Union

import logging.config

logger = logging.getLogger(__name__)


def run(argv: List[str]) -> str:
	# PENDING 結果の出力をどのような形式にすべきか
	logger.debug("コマンドライン引数: %s", argv)

	arguments, option_dict, short_options = parse_argument_vector(argv)  # PENDING ショートオプションの解析をどこでやるか

	if len(arguments) > 0:
		action_name = arguments[0]
	else:
		# PENDING -help しろよメッセージ出すか
		action_name = 'top'

	# PENDING アクションなし例外きたらエラーコード終了？
	import niascape
	return niascape.main(action_name, option_dict)  # PENDING オプション間違って unexpected keyword argument 出たらactionのhelp出す？


def parse_argument_vector(argv: List[str]) -> Tuple[List[str], Dict[str, Union[str, bool]], List[str]]:
	# PENDING urllib.parse.parse_qsのようにオプション値を全部リストにすべき？
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
				if val.isdigit():
					option_dict[key] = int(val)  # PENDING 他の型とか？
				else:
					option_dict[key] = val
			else:
				option_name = argument[2:]
		# logger.debug(argument + ': Long option')
		elif argument[0] == '-':
			logger.debug(argument + ': short option')
			short_options.append(argument[1:])
		else:
			# logger.debug(argument + ': operand')
			if option_name == '':
				arguments.append(argument)
			else:
				if argument.isdigit():
					option_dict[option_name] = int(argument)  # PENDING 他の型とか？
				else:
					option_dict[option_name] = argument
				option_name = ''

	if option_name != '':
		option_dict[option_name] = True

	return arguments[1:], option_dict, short_options  # argumentsの0を削ってwsgiと合わせる


if __name__ == '__main__':  # pragma: no cover
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(path)  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	# import json ; logging.config.dictConfig(json.load(open(path + '/tests/logger_config.json', 'r')))
	logger = logging.getLogger()

	# sys.argv.extend("daycount --site test --tag=#test --search_body test".split())

	print(run(sys.argv))
