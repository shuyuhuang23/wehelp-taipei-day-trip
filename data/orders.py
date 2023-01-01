import os
import sys
import mysql.connector

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH))
from config import Config

with mysql.connector.connect(
    user = Config.MYSQL_USER, 
    password = Config.MYSQL_PASSWORD,
    host = Config.MYSQL_HOST,
    database = Config.MYSQL_DATABASE
) as connection:
    create_db_query = '''
        CREATE TABLE IF NOT EXISTS orders (
            number                  VARCHAR(50) NOT NULL,
            user_id                 BIGINT NOT NULL,
            user_name               VARCHAR(50) NOT NULL,
            email                   VARCHAR(50) NOT NULL,
            phone                   VARCHAR(50) NOT NULL,
            price                   DECIMAL NOT NULL,           
            attraction_id           BIGINT NOT NULL,
            attraction_name         VARCHAR(50) NOT NULL,
            attraction_address      VARCHAR(50) NOT NULL,
            attraction_image        VARCHAR(1028) NOT NULL,
            `date`                  DATE NOT NULL,
            time                    VARCHAR(50) NOT NULL,
            status                  INT DEFAULT 0,
            `cre_time`              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `upd_time`              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (number)
        )
    '''
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)