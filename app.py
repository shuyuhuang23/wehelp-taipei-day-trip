from flask import *
import jwt
import mysql.connector
from config import mysqldb, config
import requests

try:
    connection = mysql.connector.connect(
        pool_name='mypool',
        pool_size=5,
        user=mysqldb.user,
        password=mysqldb.password,
        host=mysqldb.host,
        database=mysqldb.database)
except Exception as err:
    print(str(err))

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

PER_PAGE = 12
KEY = config.KEY
EXPIRE_TIME = 60 * 60 * 24 * 7


@app.route("/")
def index():
    return render_template("index.html")

# user register


@app.route("/api/user", methods=['POST'])
def register():
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        select_db_query = '''
		SELECT id FROM users
		WHERE email = %(email)s
		'''
        params = {'email': email}

        with connection.cursor() as cursor:
            cursor.execute(select_db_query, params)
            result = cursor.fetchone()

            if result:
                return {
                    "error": True,
                    "message": "此信箱已註冊過"
                }, 400

        insert_db_query = '''
		INSERT INTO users
		(
			`name`,
			email,
			password
		) VALUES (%(name)s, %(email)s, %(password)s)
		'''
        params = {'name': name, 'email': email, 'password': password}

        with connection.cursor() as cursor:
            cursor.execute(insert_db_query, params)
            connection.commit()
        return {"ok": True}
    except Exception as err:
        print(str(err))
        return {"msg": str(err)}

# get user information, login, logout


@app.route("/api/user/auth", methods=['GET', 'PUT', 'DELETE'])
def authentication():
    if request.method == 'GET':
        try:
            if 'Cookie' not in request.headers:
                return {"data": {}}
                
            token = [split_str for split_str in request.headers.get('Cookie').split() if split_str.startswith('token=')][0][6:]
            payload = jwt.decode(token, KEY, algorithms=['HS256'])

            select_db_query = '''
            SELECT id, name, email FROM users
            WHERE email = %(email)s
            '''

            params = {'email': payload['email']}

            with connection.cursor() as cursor:
                cursor.execute(select_db_query, params)
                result = cursor.fetchone()

            if result:
                return {"data": {"id": result[0], "name": result[1], "email": result[2]}}

            else:
                return {"data": {}}
        # except jwt.exceptions.InvalidSignatureError:
        #     return {"data": {}}
        except Exception as err:
            print(str(err))
            return {"data": {},
                    "message": "伺服器內部錯誤" + str(err)}
            # return {
            #     "error": True,
            #     "message": "伺服器內部錯誤" + str(err)
            # }, 500

    if request.method == 'PUT':
        try:
            email = request.json['email']
            password = request.json['password']

            select_db_query = '''
			SELECT id FROM users
			WHERE email = %(email)s AND password = %(password)s
			'''
            params = {'email': email, 'password': password}

            with connection.cursor() as cursor:
                cursor.execute(select_db_query, params)
                result = cursor.fetchone()

            if not result:
                return {
                    "error": True,
                    "message": "登入失敗，帳號或密碼錯誤"
                }, 400

            encoded_jwt = jwt.encode(
                {"email": email, "password": password}, KEY, algorithm="HS256")

            response = make_response({"ok": True})
            response.set_cookie(key='token', value=encoded_jwt,
                                max_age=EXPIRE_TIME)
            return response
        except Exception as err:
            print(str(err))
            return {
                "error": True,
                "message": "伺服器內部錯誤" + str(err)
            }, 500

    if request.method == "DELETE":
        try:
            response = make_response({"ok": True})
            response.set_cookie('token', expires=0)
            return response
        except Exception as err:
            print(str(err))
            return {
                "error": True,
                "message": "伺服器內部錯誤" + str(err)
            }, 500


@app.route("/attraction/<id>")
def show_attraction(id):
    return render_template("attraction.html")

# get all attractions with pagination and keyword search feature


@app.route("/api/attractions")
def attractions():
    try:
        page = request.args.get('page')
        keyword = request.args.get('keyword')
        offset = PER_PAGE * int(page)

        if keyword is None:
            select_db_query = "SELECT id, name, category, description, address, transport, mrt, lat, lng, images, count(*) OVER() AS cnt FROM attractions ORDER BY id LIMIT %(per_page)s OFFSET %(offset)s"
            params = {'per_page': PER_PAGE, 'offset': offset}

        else:
            select_db_query = '''
			SELECT id, name, category, description, address, transport, mrt, lat, lng, images, count(*) OVER() AS cnt
			FROM attractions
			WHERE category = %(keyword)s OR name LIKE %(fuzzy_keyword)s
			ORDER BY id
			LIMIT %(per_page)s OFFSET %(offset)s
			'''
            params = {'keyword': keyword,
                      'fuzzy_keyword': f'%{keyword}%',
                      'per_page': PER_PAGE,
                      'offset': offset}

        with connection.cursor() as cursor:
            cursor.execute(select_db_query, params)
            result = cursor.fetchall()

        next_page = int(page) + 1
        if len(result) == 0:
            next_page = None
        elif result[0][10] <= (int(page) + 1) * PER_PAGE:
            next_page = None

        return {"nextPage": next_page, "data": [{
            "id": item[0],
            "name": item[1],
            "category": item[2],
            "description": item[3],
            "address": item[4],
            "transport": item[5],
            "mrt": item[6],
            "lat": float(item[7]),
            "lng": float(item[8]),
            "images": item[9].split(',')
        } for item in result]}

    except Exception as err:
        print(str(err))
        return {
            "error": True,
            "message": "伺服器內部錯誤" + str(err)
        }, 500

# get attraction with specific id


@app.route("/api/attraction/<id>")
def attraction(id):
    try:
        with connection.cursor() as cursor:
            select_db_query = "SELECT id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions WHERE id = %(id)s"
            cursor.execute(select_db_query, {'id': id})
            result = cursor.fetchall()

        if len(result) == 0:
            return {
                "error": True,
                "message": "景點編號不正確"
            }, 400

        return {
            "data":
            {
                "id": result[0][0],
                "name": result[0][1],
                "category": result[0][2],
                "description": result[0][3],
                "address": result[0][4],
                "transport": result[0][5],
                "mrt": result[0][6],
                "lat": float(result[0][7]),
                "lng": float(result[0][8]),
                "images": result[0][9].split(',')
            }}
    except Exception as err:
        print(str(err))
        return {
            "error": True,
            "message": "伺服器內部錯誤" + str(err)
        }, 500
    # return render_template("attraction.html")

# get all categories


@app.route("/api/categories")
def categories():
    try:
        with connection.cursor() as cursor:
            select_db_query = "SELECT DISTINCT category FROM attractions"
            cursor.execute(select_db_query)
            result = cursor.fetchall()

        return {"data": [item[0] for item in result]}
    except Exception as err:
        print(str(err))
        return {
            "error": True,
            "message": "伺服器內部錯誤" + str(err)
        }, 500


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


app.run(host='0.0.0.0', port=3000)
