from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)
# データベースの接続
conn = sqlite3.connect('./syllabus.db', check_same_thread=False)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
  # キャンパスを取得
  campus = request.form.get('campus')
  print(campus)
  # 曜日を取得
  day = str(request.form.get('day'))
  # 時限を取得
  time = str(request.form.get('time'))

  print(day)
  # results = cur.execute('SELECT "教室" FROM syllabus WHERE instr("授業時間", ?) > 0;', ('day',))
  results = cur.execute('SELECT DISTINCT "教室" FROM syllabus WHERE NOT("授業時間" LIKE ? AND "授業時間" LIKE ? AND "授業時間" LIKE ?)', ('%'+day+'%', '%'+time+'%','%'+campus+'%' ))
  # datas = results.fetchall()
  print(results)
  print('検索結果')
  return render_template('search.html', results=results, campus=campus, day=day, time=time)