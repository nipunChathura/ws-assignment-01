import mysql.connector
from collections import namedtuple
from mysql.connector.connection import MySQLConnection

User = namedtuple("User", "name deposit_price lon_price guarantee_status")


def connect_db() -> MySQLConnection:
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ijse",
        database="assignment_db"
    )


class UserHelper:
    db: MySQLConnection

    def __init__(self, db):
        self.db = db

    def get_all(self):
        cur = self.db.cursor()
        sql = "select * from user"
        cur.execute(sql)
        results = cur.fetchall()
        print(results)
        users = []
        for re in results:
            print(re)
            st = User(*re)
            users.append(st)
        return users

    def insert(self, user):
        cur = self.db.cursor()
        user.guarantee_status = False
        sql = "insert into user(name, deposit_price, lon_price, guarantee_status) values(%s,%s,%s,%s)"
        cur.execute(sql, user)
        mysql.commit()
        result = cur.fetchall()
        print(result)

    def get_user_by_id(self, user_id):
        cur = self.db.cursor()
        sql = "select * from user where id=%s"
        cur.execute(sql, user_id)
        result = cur.fetchall()
        print(result)
        return result

    def get_total_amount(self):
        cur = self.db.cursor()
        sql = "select * from user"
        cur.execute(sql)
        results = cur.fetchall()
        print(results)
        total_amount = 0
        for re in results:
            total_amount += re.get("deposit_price")
        return total_amount


class LonHelper:
    db: MySQLConnection

    user_helper = UserHelper

    def __init__(self, db):
        self.db = db

    def add_lon(self, lon):
        if lon.lon_price <= self.user_helper.get_total_amount():
            cur = self.db.cursor()
            apply_user = self.user_helper.get_user_by_id(lon.apply_user_id)
            user = self.user_helper.get_user_by_id(lon.guarantee_user_id)
            if user.deposit_price <= (lon.lon_price-apply_user.deposit_price):
                user.guarantee_status = True
                sql = "insert into lon(long_id, apply_user_id, guarantee_user_id, lon_price) values(%s,%s,%s,%s)"
                cur.execute(sql, user)
                mysql.commit()
                result = cur.fetchall()
                print(result)
                return "Lon is success added"
            else:
                return "Guarantee user is not valid"
        else:
            return "Lon price Large"
