from flask import Blueprint, render_template, request, url_for
import db
import psycopg2

# Blueprint インスタンスを作成
# 第1引数は Blueprint の名前
# 第2引数はモジュール名(__name__を指定すればOK)
# 第3引数は Blueprint の URL プレフィックス
book_bp = Blueprint('book', __name__, url_prefix='/book')

# Blueprint インスタンスにルーティングを設定する。
# この場合は book_bp の url_prefix が /book なので
# このメソッドの URL は /book/list となります。
@book_bp.route('/list')
def book_list():
    book_all = db.book_list()

    # 返すHTMLは templates フォルダ以降のパスを書きます。
    return render_template('book/list.html', books=book_all)

@book_bp.route('/addition')
def book_addition():
    return render_template('addition/addition.html')

@book_bp.route('/addition', methods=['POST'])
def addition_button():
    
    # db追加
    title = request.form.get('title')
    author = request.form.get('author')
    publisher =  request.form.get('publisher')
    publicationYear = request.form.get('publicationYear')

    # if book_name == '':
    #     error = 'ユーザ名が未入力です。'
    #     return render_template('register.html', error=error, user_name=book_name, password=password)
    # if password == '':
    #     error = 'パスワードが未入力です。'
    #     return render_template('register.html', error=error)

    count = db.insert_book(title,author,publisher,publicationYear)

    # msg作成
    if count == 1:
          return render_template('mypage.html')
    else:
        return render_template('addition/addition.html')

@book_bp.route('/delete')
def book_delete():
    return render_template('delete/delete.html')

@book_bp.route('/delete2', methods=['POST'])
def delete_exe():
  id = request.form.get('id')
  
  count = db.delete_book(id)
  
      # msg作成
  if count == 1:
        return render_template('mypage.html')
  else:
        return render_template('delete/delete.html')



@book_bp.route('/update')
def book_update():
    return render_template('update/update.html')

@book_bp.route('/updates', methods=['POST'])
def update_exe():
    id=request.form.get('id')
    publisher=request.form.get('publisher')
    
    db.book_update(publisher,id)
    return render_template('mypage.html')


@book_bp.route('/search')
def book_search():
    return render_template('search/search.html')

@book_bp.route('/search2', methods=['POST'])
def search_exe():
    title = request.form.get('title')
    search_results = db.search_book(title)
    book_list = db.book_list()
    return render_template('book/list.html', books=search_results)