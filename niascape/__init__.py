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
		パッケージと同じファイル構成_test
		全テスト ファイルはある 中身を書く
"""
from datetime import datetime

now = datetime.utcnow()

import sys
import os

#Pythonスクリプトパス解決
path = os.path.dirname(os.path.abspath(__file__)).rstrip('niascape')
sys.path.append(path)

from niascape import main
run = main.run
application = main.application