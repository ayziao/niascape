#!/usr/bin/env python3
"""
コマンドラインインターフェース
"""
import os
import sys

import logging

logger = logging.getLogger(__name__)


def run(argv):
	# TODO コマンドライン引数を解決してニアスケイプRUNを実行して結果をよしなに出力
	logger.debug("コマンドライン引数: %s", argv)
	
	if len(argv) > 1:
		action = argv[1]
	else:
		# PENDING -help しろよメッセージ出すか
		action = 'top'

	# PENDING アクションなし例外きたらエラーコード終了？
	import niascape
	return niascape.run(action, argv[2:])


def parse(argv: list):
	arguments = []
	option_dict = {}
	short_options = []

	option_name = ''

	for argument in argv:
		if argument[0:2] == '--':
			if option_name != '':
				option_dict[option_name] = True
				option_name = ''
			if '=' in argument:
				c = argument[2:].split('=')
				option_dict[c[0]] = c[1]
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

	return [arguments, option_dict, short_options]


if __name__ == '__main__':  # pragma: no cover
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	# logging.basicConfig(format='\033[0;31m%(asctime)s %(name)s\n[%(levelname)s] %(message)s\033[0m', level=logging.DEBUG)

	# sys.argv.extend("daycount test #test test".split())
	# sys.argv.extend("action test #test test".split())

	print(run(sys.argv))
	
	# print(sys.argv)
	# 
	# print(parse(sys.argv))
	# 
	# 
	# 
	# parsed = parse(sys.argv)
	# arguments = parsed[0]
	# option_dict = parsed[1]
	# short_options = parsed[2]
