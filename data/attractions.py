import os
import sys
import re
import json
import mysql.connector

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH, 'config'))
import mysqldb

def extract_img_str(raw_str):
    lst_str = re.findall(r'(http.*?(.jpg|.JPG|.png|.PNG))', raw_str)
    img_file_str = ','.join([str[0] for str in lst_str])
    return img_file_str

with open('taipei-attractions.json', 'r') as f:
    data = json.load(f)
data = data['result']['results']

val = [(item['_id'], item['rate'], item['direction'], item['name'], item['date'], 
        item['longitude'], item['latitude'], item['MRT'], item['CAT'], 
        item['MEMO_TIME'], extract_img_str(item['file']), item['description'], item['address']) for item in data]

with mysql.connector.connect(
    user = mysqldb.user, 
    password = mysqldb.password,
    host = mysqldb.host,
    database = mysqldb.database
) as connection:
    create_db_query = '''
        CREATE TABLE IF NOT EXISTS attractions (
            id          BIGINT AUTO_INCREMENT,
            rate        INT NOT NULL,
            transport   NVARCHAR(3000) NOT NULL,
            `name`      NVARCHAR(255) NOT NULL,
            date        DATE NOT NULL,
            lng         DECIMAL(9,6) NOT NULL,
            lat         DECIMAL(9,6) NOT NULL,
            mrt         NVARCHAR(255) DEFAULT NULL,
            category    NVARCHAR(255) NOT NULL,
            memo        NVARCHAR(3000) DEFAULT NULL,
            images      NVARCHAR(3000) NOT NULL,
            description NVARCHAR(3000) NOT NULL,
            address     NVARCHAR(255) NOT NULL,
            `time`      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
    '''
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)
    
    insert_db_query = '''INSERT INTO attractions 
        (
            id,
            rate,
            transport,
            `name`,
            date,
            lng,
            lat,
            mrt,
            category,
            memo,
            images,
            description,
            address
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    with connection.cursor() as cursor:
        cursor.executemany(insert_db_query, val)
        connection.commit()
    

