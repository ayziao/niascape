"""
メインモジュール

packageの__init__.pyで読み込んでるのでコマンドラインから直接実行する時ぐらいかな
"""

# TODO メインモジュールの説明書く

def run() -> str:
	"""
	# コマンドライン向け
	@return:
	"""
	return 'main'


if __name__ == '__main__':
	print(run())  # pragma: no cover
