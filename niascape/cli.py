#!/usr/bin/env python3
"""
コマンドラインインターフェース
"""
import os
import sys

import logging

logger = logging.getLogger(__name__)


def cli():
	# TODO コマンドライン引数を解決してニアスケイプRUNを実行して結果をよしなに出力
	logger.debug("コマンドライン引数: %s", sys.argv)

	if len(sys.argv) > 1:
		action = sys.argv[1]
	else:
		# PENDING -help しろよメッセージ出すか
		action = 'top'

	# PENDING アクションなし例外きたらエラーコード終了？
	import niascape
	return niascape.run(action)


if __name__ == '__main__':  # pragma: no cover
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる

	# sys.argv.append('daycount')

	print(cli())
