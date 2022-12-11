import os
import sys
import re
import json
import mysql.connector

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH, 'config'))
import mysqldb

# val = [('彭彭', 'peng@mail.com', 'wehelp'), ('user', 'user@mail.com', 'user')]

with mysql.connector.connect(
    user = mysqldb.user, 
    password = mysqldb.password,
    host = mysqldb.host,
    database = mysqldb.database
) as connection:
    create_db_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id            BIGINT AUTO_INCREMENT,
            `name`        NVARCHAR(255) NOT NULL,
            email         VARCHAR(50) NOT NULL,
            password      CHAR(128) NOT NULL,
            `cre_time`    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `upd_time`    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (email),
            PRIMARY KEY (id)
        )
    '''
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)
    
    # insert_db_query = '''INSERT INTO users 
    #     (
    #         `name`,
    #         email,
    #         password
    #     ) VALUES (%s, %s, %s)
    # '''
    # with connection.cursor() as cursor:
    #     cursor.executemany(insert_db_query, val)
    #     connection.commit()
    

