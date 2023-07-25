import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(user_name, password):
    sql = 'INSERT INTO user_sample VALUES(default, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM user_sample WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password = get_hash(password, salt)

            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg

def insert_book(title, author, publisher, publication_year):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "insert into book values(default, %s, %s, %s, %s)"
        
        cursor.execute(sql, (title, author, publisher, publication_year))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
        
    finally:
        cursor.close()
        connection.close()
    
    return count

def book_list():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM book ORDER BY id ASC"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def delete_book(id):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = " delete from book where id = %s"
        
        cursor.execute(sql, (id,))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
        
    finally:
        cursor.close()
        connection.close()
    
    return count   
        
def book_update(publisher, id):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql="update book set publisher = %s where id = %s"
        
    cursor.execute(sql, (publisher, id))
    connection.commit() 
    
    cursor.close()
    connection.close()
 
def search_book(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM book WHERE title LIKE %s"
    
    title_pattern="%" + title + "%"
    cursor.execute(sql, (title_pattern,))
    results = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return results      