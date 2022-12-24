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
        CREATE TABLE IF NOT EXISTS appointments (
            id               BIGINT AUTO_INCREMENT,
            user_id          BIGINT NOT NULL,
            attraction_id    BIGINT NOT NULL,
            `date`           DATE NOT NULL,
            time             VARCHAR(50) NOT NULL,
            price            DECIMAL NOT NULL,
            `cre_time`       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `upd_time`       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
    '''
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)