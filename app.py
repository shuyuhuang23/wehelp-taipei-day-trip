from flask import *
import mysql.connector
from config import mysqldb

connection = mysql.connector.connect(
	user = mysqldb.user,
	password = mysqldb.password,
	host = mysqldb.host,
	database = mysqldb.database)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Pages
PER_PAGE = 12

@app.route("/")
def index():
	return render_template("index.html")

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

	except:
		return {
			"error": True,
			"message": "伺服器內部錯誤"
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
	except:
		return {
			"error": True,
			"message": "伺服器內部錯誤"
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
	except:
		return {
			"error": True,
			"message": "伺服器內部錯誤"
		}, 500


@app.route("/booking")
def booking():
	return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.run(port = 3000)
