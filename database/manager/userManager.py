import hashlib
from enum import Enum

import mysql.connector
import database.core as core

class Role(Enum):
    teacher = "teacher"
    student = "student"

def create_user(dbase: core.core, username, password, full_name, role: Role):
    dbase.db_connection.connect()
    cursor = dbase.db_connection.cursor()
    success = False
    try:
        cursor.execute(f"""
            INSERT INTO quiz.users (username, password_hash, full_name, role) VALUES (
                '{username}',
                '{hash_password(password)}',
                '{full_name}',
                '{role.value}'
            );
            """)
        dbase.db_connection.commit()
        success = True
    except mysql.connector.Error as err:
            print(err)

    if success:  # success
        print("User created successfully.")
    else:
        print("User creation failed. Please try again.")


def getUserRole(dbase: core.core, user_id: int):
    try:
        cursor = dbase.db_connection.cursor()
        cursor.execute("SELECT role FROM quiz.users WHERE user_id = '%s'" % (user_id,))
        role = cursor.fetchone()
        if role:
            return role
        else:
            return False
    except mysql.connector.Error as err:
        print(err)
    return False

def getUseridByUsername(dbase: core.core, username):
    try:
        cursor = dbase.db_connection.cursor()
        cursor.execute("SELECT user_id FROM quiz.users WHERE username = '%s'" % (username,))
        data = cursor.fetchone()
        if data:
            return data[0]
    except mysql.connector.Error as err:
        print(err)
    return False

def verify_user(dbase: core.core, username, password):
    cursor = dbase.db_connection.cursor()
    try:
        cursor.execute("SELECT user_id,full_name,role FROM quiz.users WHERE username = '%s' AND password_hash = '%s'" % (username, hash_password(password),))
        data = cursor.fetchone()
        if data:
            return True,data
        else:
            return False, None
    except mysql.connector.Error as err:
        print(err)
    return False, None

def getUsernameByID(dbase: core.core, user_id: int):
    cursor = dbase.db_connection.cursor()
    try:
        cursor.execute("SELECT full_name FROM quiz.users WHERE user_id = '%s'" % (user_id,))
        data = cursor.fetchall()
        if data:
            return True, data[0][0]
        else:
            return False, None
    except mysql.connector.Error as err:
        return False, err

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()