#!/home/xs471697/.pyenv/versions/anaconda3-5.3.1/bin/python3

import cgi
import sys
import io
from spcy_test import main
 
# 日本語を受信時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
 
form = cgi.FieldStorage()
 
# 入力チェック（必要な変数が送信されていない場合はエラー。）
if 'your_name' not in form:
    print('Content-type: text/html; charset=UTF-8')
    print('')
    print('your_name フィールドが送信されていません。')
    sys.exit()
 
# your_name の値を取得して変数にセット。
# 値が入力されていない場合は「匿名」を設定。
your_name = form.getvalue('your_name', '匿名')
 
# 入力チェック（yourname が 2 個以上送信されている場合はエラー。）
if isinstance(your_name, list):
    print('Content-type: text/html; charset=UTF-8')
    print('')
    print('your_name フィールドが 2 個以上送信されています。')
    sys.exit()

 
# テキストファイルとして内容を出力
print('Content-type: text/html; charset=UTF-8')
print('')
print(your_name)