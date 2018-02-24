"""
メインモジュール

packageの__init__.pyで読み込んでるのでコマンドラインから直接実行する時ぐらいかな
"""

# TODO メインモジュールの説明書く
from configparser import ConfigParser


def run() -> str:
	"""
	# コマンドライン向け
	@return:
	"""
	return 'main'



def readini(path='config.ini'):
	ini = ConfigParser()
	ini.read(path)
	return ini


if __name__ == '__main__':
	print(run())  # pragma: no cover
