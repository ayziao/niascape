#!/usr/bin/env python3
"""
コマンドラインインターフェース
"""
import os
import sys
from typing import List, Tuple, Dict, Union
import logging

logger = logging.getLogger(__name__)


def run(argv: List[str]) -> str:
	# TODO コマンドライン引数を解決してニアスケイプRUNを実行して結果をよしなに出力
	logger.debug("コマンドライン引数: %s", argv)

	arguments, option_dict, short_options = parse_argument_vector(argv)  # PENDING ショートオプションの解析をどこでやるか

	if len(arguments) > 1:
		action_name = arguments[1]
	else:
		# PENDING -help しろよメッセージ出すか
		action_name = 'top'

	# PENDING アクションなし例外きたらエラーコード終了？
	import niascape
	return niascape.run(action_name, option_dict)  # PENDING オプション間違って unexpected keyword argument 出たらactionのhelp出す？


def parse_argument_vector(argv: List[str]) -> Tuple[List[str], Dict[str, Union[str, bool]], List[str]]:
	# PENDING urllib.parse.parse_qsのようにオプション値を全部リストにすべき？
	arguments = []
	option_dict = {} # type: Dict[str,Union[str,bool]]
	short_options = []

	option_name = ''

	for argument in argv:
		if argument[0:2] == '--':
			if option_name != '':
				option_dict[option_name] = True
				option_name = ''
			if '=' in argument:
				key, val = argument[2:].split('=')
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
				option_dict[option_name] = argument
				option_name = ''

	if option_name != '':
		option_dict[option_name] = True

	return (arguments, option_dict, short_options)


if __name__ == '__main__':  # pragma: no cover
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	# logging.basicConfig(format='\033[0;31m%(asctime)s %(name)s\n[%(levelname)s] %(message)s\033[0m', level=logging.DEBUG)

	sys.argv.extend("daycount --site test --tag=#test --search_body test".split())
	# sys.argv.extend("action test #test test".split())

	print(run(sys.argv))
