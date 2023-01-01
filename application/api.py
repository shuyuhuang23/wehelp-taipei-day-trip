from flask import Blueprint
from flask import request
from flask import make_response
from flask import current_app
import jwt
import requests

from application import mysql_db

PER_PAGE = 12
config = current_app.config
api_bp = Blueprint('api', __name__)


def identify_auth(request):
    try:
        if 'Cookie' not in request.headers:
            return {"data": {}}

        token = [split_str for split_str in request.headers.get(
            'Cookie').split() if split_str.startswith('token=')][0][6:]
        payload = jwt.decode(token, config['SECRET_KEY'], algorithms=['HS256'])

        select_db_query = '''
        SELECT id, name, email FROM users
        WHERE email = %(email)s
        '''

        params = {'email': payload['email']}

        with mysql_db.cnn.cursor() as cursor:
            cursor.execute(select_db_query, params)
            result = cursor.fetchone()

        if result:
            return {"data": {"id": result[0], "name": result[1], "email": result[2]}}

        else:
            return {"data": {}}
    # except jwt.exceptions.InvalidSignatureError:
    #     return {"data": {}}
    except Exception as err:
        return {"data": {},
                "message": "伺服器內部錯誤" + str(err)}


def delete_booking(user_id):
    delete_db_query = '''
        DELETE FROM appointments
        WHERE user_id = %(user_id)s
        '''
    params = {'user_id': user_id}

    with mysql_db.cnn.cursor() as cursor:
        cursor.execute(delete_db_query, params)
        mysql_db.cnn.commit()
    return


@api_bp.route("/user", methods=['POST'])
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

        with mysql_db.cnn.cursor() as cursor:
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

        with mysql_db.cnn.cursor() as cursor:
            cursor.execute(insert_db_query, params)
            mysql_db.cnn.commit()
        return {"ok": True}

    except Exception as err:
        return {
            "error": True,
            "message": "伺服器內部錯誤" + str(err)
        }, 500


@api_bp.route("/user/auth", methods=['GET', 'PUT', 'DELETE'])
def authentication():
    if request.method == 'GET':
        try:
            return identify_auth(request)

        except Exception as err:
            return {"data": {},
                    "message": "伺服器內部錯誤" + str(err)}

    if request.method == 'PUT':
        try:
            email = request.json['email']
            password = request.json['password']

            select_db_query = '''
			SELECT id FROM users
			WHERE email = %(email)s AND password = %(password)s
			'''
            params = {'email': email, 'password': password}

            with mysql_db.cnn.cursor() as cursor:
                cursor.execute(select_db_query, params)
                result = cursor.fetchone()

            if not result:
                return {
                    "error": True,
                    "message": "登入失敗，帳號或密碼錯誤"
                }, 400

            encoded_jwt = jwt.encode(
                {"email": email, "password": password}, config['SECRET_KEY'], algorithm="HS256")

            response = make_response({"ok": True})
            response.set_cookie(key='token', value=encoded_jwt,
                                max_age=config['COOKIE_EXPIRE_TIME'])
            return response
        except Exception as err:
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
            return {
                "error": True,
                "message": "伺服器內部錯誤" + str(err)
            }, 500


@api_bp.route('/attractions')
def attractions():
    try:
        page = request.args.get('page')
        keyword = request.args.get('keyword')
        offset = PER_PAGE * int(page)

        if keyword is None:
            select_db_query = '''
            SELECT id, name, category, description, address, transport, mrt, lat, lng, images, count(*) OVER() AS cnt 
            FROM attractions ORDER BY id LIMIT %(per_page)s OFFSET %(offset)s
            '''
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

        with mysql_db.cnn.cursor() as cursor:
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
        return {
            "error": True,
            "message": "伺服器內部錯誤" + str(err)
        }, 500


@api_bp.route('/attraction/<id>')
def attraction(id):
    try:
        with mysql_db.cnn.cursor() as cursor:
            select_db_query = '''
            SELECT id, name, category, description, address, transport, mrt, lat, lng, images 
            FROM attractions WHERE id = %(id)s
            '''
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

# get all categories


@api_bp.route('/categories')
def categories():
    try:
        with mysql_db.cnn.cursor() as cursor:
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


@api_bp.route("/booking", methods=['GET', 'POST', 'DELETE'])
def create_appointment():
    if request.method == 'GET':

        user_info = identify_auth(request)

        if len(user_info) == 0:
            return {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }, 403

        user_id = user_info['data']['id']

        select_db_query = '''
        SELECT id, name, address, images, date, time, price FROM
        (
            SELECT attraction_id, date, time, price FROM appointments
            WHERE user_id = %(user_id)s
        ) app JOIN
        (
            SELECT id, name, address, images FROM attractions
        ) att
        ON app.attraction_id = att.id
        '''
        params = {'user_id': user_id}

        with mysql_db.cnn.cursor() as cursor:

            cursor.execute(select_db_query, params)
            result = cursor.fetchone()

        if result is None:
            return {"data": {}}

        return {"data": {
            "attraction": {
                "id": result[0],
                "name": result[1],
                "address": result[2],
                "image": result[3].split(',')[0]
            },
            "date": result[4].strftime("%Y-%m-%d"),
            "time": result[5],
            "price": result[6]
        }}

    if request.method == 'POST':
        try:
            user_info = identify_auth(request)

            if len(user_info) == 0:
                return {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                }, 403

            user_id = user_info['data']['id']
            attraction_id = request.json['attractionId']
            date = request.json['date']
            time = request.json['time']
            price = request.json['price']

            delete_booking(user_id)

            insert_db_query = '''
            INSERT INTO appointments
            (
                user_id,
                attraction_id,
                date,
                time,
                price
            ) VALUES (%(user_id)s, %(attraction_id)s, %(date)s, %(time)s, %(price)s)
            '''
            params = {'user_id': user_id, 'attraction_id': attraction_id,
                      'date': date, 'time': time, 'price': price}

            with mysql_db.cnn.cursor() as cursor:
                cursor.execute(insert_db_query, params)
                mysql_db.cnn.commit()

            return {"ok": True}
        except Exception as err:
            return {
                "error": True,
                "message": "伺服器內部錯誤" + str(err)
            }, 500

    if request.method == 'DELETE':
        try:
            user_info = identify_auth(request)

            if len(user_info) == 0:
                return {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                }, 403

            user_id = user_info['data']['id']

            delete_booking(user_id)

            return {"ok": True}
        except Exception as err:
            return {
                "error": True,
                "message": "伺服器內部錯誤" + str(err)
            }, 500


@api_bp.route("/order/<order_number>")
def order_info(order_number):
    try:
        user_info = identify_auth(request)

        if len(user_info) == 0:
            return {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }, 403

        select_db_query = '''
        SELECT * FROM orders
        WHERE number = %(order_number)s
        '''

        params = {'order_number': order_number}

        with mysql_db.cnn.cursor() as cursor:
            cursor.execute(select_db_query, params)
            result = cursor.fetchone()

        if result is None:
            return {"data": {}}
        else:
            return {"data": {
                "number": order_number,
                "price": result[1],
                "trip": {
                    "attraction": {
                        "id": result[6],
                        "name": result[7],
                        "address": result[8],
                        "image": result[9]
                    },
                    "date": result[10].strftime("%Y-%m-%d"),
                    "time": result[11]
                },
                "contact": {
                "name": result[2],
                "email": result[3],
                "phone": result[4]
                },
                "status": result[12]
            }}
    except Exception as err:
            return {
                "error": True,
                "message": "伺服器內部錯誤" + str(err)
            }, 500




@api_bp.route("/orders", methods=['POST'])
def create_order():

    user_info = identify_auth(request)

    if len(user_info) == 0:
        return {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }, 403

    user_id = user_info['data']['id']

    # url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
    # PARTNER_KEY = 'partner_bvDf8QbqUoHRuPKultmC2gA8XU4WDMkUH7aCobocr56VSK8MbiGM3nud'
    # MERCHANT_ID = 'wehelp_ESUN'
    prime = request.json['prime']
    user_name = request.json['order']['contact']['name']
    email = request.json['order']['contact']['email']
    phone = request.json['order']['contact']['phone']
    attraction_id = request.json['order']['trip']['attraction']['id']
    attraction_name = request.json['order']['trip']['attraction']['name']
    attraction_address = request.json['order']['trip']['attraction']['address']
    attraction_image = request.json['order']['trip']['attraction']['image']
    date = request.json['order']['trip']['date']
    time = request.json['order']['trip']['time']
    price = request.json['order']['price']

    data = {
        'prime': prime,
        'partner_key': config['PARTNER_KEY'],
        'merchant_id': config['MERCHANT_ID'],
        'amount': price,
        "details": "TapPay Test",
        "cardholder": {
            "phone_number": phone,
            "name": user_name,
            "email": email
        }
    }
    response = requests.post(config['PAY_URL'], json = data, headers = {'x-api-key': config['PARTNER_KEY']}).json()


    number = response['rec_trade_id']
    
    insert_db_query = '''
        INSERT INTO orders
        (
            number,
            user_id,
            user_name,
            email,
            phone,
            price,
            attraction_id,
            attraction_name,
            attraction_address,
            attraction_image,
            `date`,
            time,
            status
        ) VALUES (
            %(number)s, 
            %(user_id)s, 
            %(user_name)s, 
            %(email)s, 
            %(phone)s, 
            %(price)s, 
            %(attraction_id)s, 
            %(attraction_name)s,
            %(attraction_address)s,
            %(attraction_image)s,  
            %(date)s, 
            %(time)s,
             %(status)s)
        '''
    params = {'number': number, 
        'user_id': user_id, 
        'user_name': user_name,
        'email': email,
        'phone': phone,
        'price': price,
        'attraction_id': attraction_id,
        'attraction_name': attraction_name,
        'attraction_address': attraction_address,
        'attraction_image': attraction_image,
        'date': date,
        'time': time,
        'status': response['status']
    }

    with mysql_db.cnn.cursor() as cursor:
        cursor.execute(insert_db_query, params)
        mysql_db.cnn.commit()

    if response['status'] == 0:
        delete_db_query = '''
        DELETE FROM appointments
        WHERE user_id = %(user_id)s
        '''
        params = {'user_id': user_id}

        with mysql_db.cnn.cursor() as cursor:
            cursor.execute(delete_db_query, params)
            mysql_db.cnn.commit()

        return {
            "data": {
                "number": response['rec_trade_id'],
                "payment": {
                    "status": 0,
                    "message": "付款成功"
                }
            }
        }
    else:
        return {
            "error": True,
            "message": response.msg
        }, 400
