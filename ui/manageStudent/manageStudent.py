import mysql.connector
from tabulate import tabulate

from database.core import core
from database.manager import userManager
from ui.dashboard import teacher_dashboard


def createUser(database: core, userid):
    fullname = input("Please enter user's full name: ")
    username = input("Enter user's username: ")
    password = input("Enter user's password: ")
    role = input("Enter user's role (Teacher/Student): ")
    if len(fullname) > 100:
        print("Full Name must be less than 100 characters")
    elif len(username) > 50:
        print("Username must be less than 50 characters")
    elif role.lower() not in ["teacher", "student"]:
        print("Role must be 'teacher' or 'student'")
    else:
        try:
            cursor = database.db_connection.cursor()
            cursor.execute(f"SELECT * FROM quiz.users WHERE username='{username}'")
            data = cursor.fetchone()
            if data is None:
                cursor.execute(f"INSERT INTO quiz.users (username,password_hash,full_name, role) VALUES ("
                               f"'{username}','{userManager.hash_password(password)}','{fullname}','{role}');")
                database.db_connection.commit()
                print("User created successfully!")
            else:
                print("User already exists! Please try using another username")
        except mysql.connector.Error:
            print("Failed to create a new user, please try again.")

    input("Press any key to continue...")
    teacher_dashboard(database, userid)

def deleteUser(database: core, userid):
    username = input("Please enter user's username: ")
    try:
        cursor = database.db_connection.cursor()
        cursor.execute(f"SELECT full_name FROM quiz.users WHERE username='{username}'")
        data = cursor.fetchone()
        if data:
            confirm = input(f"Are you sure you want to delete {data[0]}? (y/n): ")
            if confirm.lower() == "y":
                cursor.execute(f"DELETE FROM quiz.users WHERE username='{username}'")
                database.db_connection.commit()
                print("User deleted successfully!")
            else:
                print("Action cancelled!")
        else:
            print("User not found!")
    except mysql.connector.Error:
        print("Failed to delete a user, please try again.")

    input("Press any key to continue...")
    teacher_dashboard(database, userid)

def viewAllUsers(database: core, userid):
    cursor = database.db_connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM quiz.users;")
        data = cursor.fetchall()
        datas = []
        for i in data:
            userid = i[0]
            username = i[1]
            fullname = i[3]
            role = i[4]
            createTime = i[5]
            datas.append([userid, username, fullname, role, createTime])
        header = ["User ID", "Username", "Full Name", "Role", "Create Time"]
        print(tabulate(datas, headers=header, tablefmt="grid"))
    except mysql.connector.Error as err:
        print(err)
        print("Failed to view a user, please try again.")

    input("Press any key to go back...")
    teacher_dashboard(database, userid)





