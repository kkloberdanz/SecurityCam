from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from app import login


def create_hash(password):
    return generate_password_hash(password)


def check_password(username, password):
    sql = "select password_hash from user where username=?"
    try:
        dbc = sqlite3.connect('db').cursor()
        (db_hash,) = dbc.execute(sql, [username]).fetchone()
    finally:
        dbc.close()
    return check_password_hash(db_hash, password)
