"""
メインモジュール

# TODO メインモジュールの説明書く
"""
import os
import sys
import datetime
import json

import logging

logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

import niascape
from niascape.entity import basedata


def run(action='top', option={}) -> str:  # PENDING __ini__に移動するか
	logger.debug("アクション: %s", action)
	# TODO elif連打やめる
	if action == 'top':
		return 'top'
	elif action == 'daycount':
		return json.dumps(basedata._daycount())  # PENDING どこでJSON化すべきか
	else:
		# TODO 例外を投げる
		return 'No Action'


if __name__ == '__main__':  # pragma: no cover
	logging.basicConfig(format='%(asctime)s %(name)s\n[%(levelname)s] %(message)s', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる

	logger.debug("開始時刻(UTC): %s", niascape.init_time)

	logger.debug("実行中のスクリプトへの相対パス: %s", __file__)
	logger.debug("実行中のスクリプトへの絶対パス: %s", os.path.abspath(__file__))

	# sys.argv.append('daycount')

	print(niascape.cli())

	logger.debug("終了時刻(UTC): %s", datetime.datetime.utcnow())
