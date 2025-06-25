import os
from core.settings import settings
import pymysql
import psycopg2

def create_db():
    """데이터베이스를 생성합니다."""



    def create_mysql():
        host = settings.DB_HOST
        port = settings.DB_PORT
        user = settings.DB_USER
        password = settings.DB_PASSWORD
        db_name = settings.DB_NAME
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        print(f"MySQL DB `{db_name}` 생성 또는 이미 존재합니다.")
        conn.close()
    def create_test_mysql():
        host = settings.TEST_DB_HOST
        port = settings.TEST_DB_PORT
        user = settings.TEST_DB_USER
        password = settings.TEST_DB_PASSWORD
        db_name = settings.TEST_DB_NAME
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        print(f"MySQL DB `{db_name}` 생성 또는 이미 존재합니다.")
        conn.close()


    def create_postgresql():
        host = settings.DB_HOST
        port = settings.DB_PORT
        user = settings.DB_USER
        password = settings.DB_PASSWORD
        db_name = settings.DB_NAME
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname="postgres")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_name};")
            print(f"PostgreSQL DB `{db_name}` 생성 완료.")
        else:
            print(f"PostgreSQL DB `{db_name}` 이미 존재합니다.")
        conn.close()

    def create_test_postgresql():
        host = settings.TEST_DB_HOST
        port = settings.TEST_DB_PORT
        user = settings.TEST_DB_USER
        password = settings.TEST_DB_PASSWORD
        db_name = settings.TEST_DB_NAME
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname="postgres")
        conn.autocommit = True

    if settings.DEBUG:
        if settings.DB_TYPE.lower() == "mysql":
            create_mysql()
            create_test_mysql()
        elif settings.DB_TYPE.lower() == "postgresql":
            create_postgresql()
            create_test_postgresql()
    else:
        if settings.DB_TYPE.lower() == "mysql":
            create_mysql()
        elif settings.DB_TYPE.lower() == "postgresql":
            create_postgresql()
        

if __name__ == "__main__":
    create_db()