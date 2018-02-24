"""
niascape パッケージ

パッケージ名/ 済み
	パッケージ名/ 済み
		メイン 済み
		サブパッケージ/
	セットアップ
	りーどみー ファイルはある 中身を書く
	ライセンス 済み

	ドキュメント/ 必要になったら
	ユニットテスト/ 済み
		パッケージと同じディレクトリ構成
		test_パッケージと同じファイル構成
		全テスト ファイルはある 中身を書く
"""
import os
from datetime import datetime
from configparser import ConfigParser

from niascape import main
from niascape import wsgiapplication

init_time = datetime.utcnow()


def _readini(file_name='config.ini'):
	# PENDING フルパス受け付けるか検討
	# PENDING config.ini が無い時 config.ini.sample を読むか検討
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	ini = ConfigParser()
	ini.read(path + '/' + file_name)
	return ini


ini = _readini()

run = main.run
application = wsgiapplication.application
