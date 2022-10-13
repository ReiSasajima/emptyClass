from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# # データベースの接続
# conn = sqlite3.connect('./ranking.db', check_same_thread=False)
# cur = conn.cursor()
@app.route('/', methods=['POST', 'GET'])
def search():
  if request.method == 'GET':
    return render_template('search.html')
  elif request.method == 'POST':
    # キャンパスを取得
    campus = request.form.get('campus')
    # 曜日を取得
    day = request.form.get('day')
    # 時限を取得
    time = request.form.get('time')
    print(campus, day, time)

