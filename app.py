from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta
from book import book_bp

import book

app = Flask(__name__)
app.secret_key=''.join(random.choices(string.ascii_letters, k=256))

app.register_blueprint(book_bp)


@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    # ログイン判定
    if db.login(user_name, password):
        session['user'] =True
        session.permanent=True
        app.permanent_session_lifetime=timedelta(minutes=30) # session の有効期限を 30 分に設定
        return redirect(url_for('mypage'))
    else :
        error = 'ユーザ名またはパスワードが違います。'

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/mypage', methods=['GET'])
def mypage():
 if 'user' in session:
    return render_template('mypage.html')
 else :
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, user_name=user_name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)




#戻る
@app.route('/back_form')
def back_form():
    return render_template('mypage.html')


if __name__ == '__main__':
    app.run(debug=True)