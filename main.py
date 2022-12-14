from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)
# データベースの接続
conn = sqlite3.connect('./syllabus.db', check_same_thread=False)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
  if request.method == 'GET':
    return redirect('/')
  if request.method == 'POST':
    # キャンパスを取得
    campus = request.form.get('campus')
    print(campus)
    # 前期か後期かの判定
    term = str(request.form.get('term'))
    print(term)
    # 曜日を取得
    day = str(request.form.get('day'))
    # 時限を取得
    time = str(request.form.get('time'))

    key = day+time
    print(key)
    # results = cur.execute('SELECT "教室" FROM syllabus WHERE instr("授業時間", ?) > 0;', ('day',))
    results = cur.execute('''SELECT "授業時間", "授業名", "教室" 
                          FROM syllabus 
                          WHERE "授業時間" LIKE ? /*キャンパス*/
                          AND "授業時間" LIKE ? /*前期後期が該当する*/
                          AND "授業時間" NOT LIKE ? /*授業時限が該当しない*/
                          AND "授業時間"  NOT LIKE "不定" /*「不定」を削除*/
                          AND "授業名"  NOT LIKE "オンライン" /*「オンライン」を削除*/
                          AND "教室" NOT LIKE "None" /*教室名が「None」を削除*/
                          AND "授業時間" NOT LIKE ? /*時期が「通年」を削除*/
                          GROUP BY "教室" ''' , 
                          (
                          '%'+campus+'%', 
                          '%'+term+'%',
                          '%'+key+'%',
                          '%'+'通年'+'%',
                          ))
    print(results)
    print('検索結果')
    return render_template('search.html', results=results, campus=campus, day=day, time=time, term=term)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)