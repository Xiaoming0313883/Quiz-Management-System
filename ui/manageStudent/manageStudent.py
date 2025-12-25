import mysql.connector
from tabulate import tabulate

from asset.useful import clear_console
from database.core import core
from database.manager import userManager
import ui.dashboard as dashboard


def createUser(database: core, userid):
    clear_console()
    print("User Creation\n")
    fullname = input("Please enter user's full name: ")
    username = input("Enter user's username: ")
    password = input("Enter user's password: ")
    role = input("Enter user's role (Teacher/Student): ")
    if len(fullname) == 0:
        print("Full Name cannot be empty!")
    elif len(username) == 0:
        print("Username cannot be empty!")
    elif len(password) == 0:
        print("Password cannot be empty!")
    elif len(role) == 0:
        print("Role cannot be empty!")
    elif len(fullname) > 100:
        print("Full Name must be less than 100 characters")
    elif len(username) > 50:
        print("Username must be less than 50 characters")
    elif username.count(" ") >= 1:
        print("Username cannot contain spaces!")
    elif role.lower() not in ["teacher", "student"]:
        print("Role must be 'teacher' or 'student'")
    else:
        try:
            cursor = database.db_connection.cursor()
            cursor.execute("SELECT * FROM quiz.users WHERE username='%s'" % (username,))
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
    dashboard.teacher_dashboard(database, userid)

def deleteUser(database: core, userid):
    clear_console()
    print("User deletion\n")
    username = input("Please enter user's username: ")
    try:
        cursor = database.db_connection.cursor()
        cursor.execute("SELECT full_name FROM quiz.users WHERE username='%s'" % (username,))
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
    dashboard.teacher_dashboard(database, userid)

def viewAllUsers(database: core, userid):
    clear_console()
    cursor = database.db_connection.cursor()
    try:
        cursor.execute("SELECT * FROM quiz.users;")
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
        print("\nAll user list:")
        print(tabulate(datas, headers=header, tablefmt="grid"))
    except mysql.connector.Error as err:
        print(err)
        print("Failed to view a user, please try again.")

    input("Press any key to go back...")
    dashboard.teacher_dashboard(database, userid)





