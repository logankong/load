import pymysql
import traceback


class DB():
    def __init__(self):
        self.db_host = '10.18.208.226'
        self.db_port = 3306
        self.db_user = 'mysql'
        self.db_pwd = '360tianxun#^)Sec'
        self.db_name = 'WIPS'

        SQL_Config = {
            'host': self.db_host,
            'port': self.db_port,
            'user': self.db_user,
            'passwd': self.db_pwd,
            'db': self.db_name,
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
        }

        try:
            self.conn = pymysql.Connect(**SQL_Config)
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def insert(self, sqlString, *args):
        try:
            self.cursor.execute(sqlString, *args)
            self.conn.commit()
        except:
            traceback.print_exc()
            print("insert failed.")

    def getOne(self, sqlString, *args):
        try:
            self.cursor.execute(sqlString, *args)
            data = self.cursor.fetchone()
            return data
        except:
            import traceback
            traceback.print_exc()
            print(sqlString + ' execute failed.')

    def getAll(self, sqlString, *args):
        try:
            self.cursor.execute(sqlString, *args)
            data = self.cursor.fetchall()
            return data
        except:
            import traceback
            traceback.print_exc()
            print(sqlString + ' execute failed.')

    def update(self, sqlString, *args):
        try:
            self.cursor.execute(sqlString, *args)
            self.conn.commit()
        except:
            print(sqlString + ' update failed.')

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()


if __name__ == "__main__":
    db = DB('127.0.0.1', 3306, 'root', '123456', 'world')
    print(db.query("show tables;"))
