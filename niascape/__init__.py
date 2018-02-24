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
import sys
import os
from datetime import datetime

from niascape import main
from niascape import wsgiapplication

init_time = datetime.utcnow()

run = main.run
application = wsgiapplication.application
