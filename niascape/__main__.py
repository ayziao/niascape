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
from niascape import action


def run(action_name='top', option=None) -> str:  # PENDING __ini__に移動するか
	logger.debug("アクション: %s", action_name)

	try:
		m = getattr(action, action_name)
	except AttributeError:
		return _no_action(action_name)

	if callable(m):
		return m(option)
	else:
		return _no_action(action_name)


def _no_action(action_name):
	# TODO 例外を投げる
	logger.info("アクションなし: %s", action_name)  # PENDING インフォかワーニングか設定で変えられるようにすべきか
	return 'No Action'


if __name__ == '__main__':  # pragma: no cover
	logging.basicConfig(format='\033[0;31m%(asctime)s %(name)s\n[%(levelname)s] %(message)s\033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる

	logger.debug("開始時刻(UTC): %s", niascape.init_time)

	logger.debug("実行中のスクリプトへの相対パス: %s", __file__)
	logger.debug("実行中のスクリプトへの絶対パス: %s", os.path.abspath(__file__))

	# sys.argv.append('daycount')

	print(niascape.cli())

	logger.debug("終了時刻(UTC): %s", datetime.datetime.utcnow())
