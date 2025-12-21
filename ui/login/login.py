from asset.useful import clear_console
from database.manager import userManager
from database.core import core
from ui.dashboard import dashboard


def login(database: core):
    clear_console()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    verify, data = userManager.verify_user(database, username, password)
    if verify:
        dashboard(database, data)
    else:
        print("Username or password is incorrect! Please try again.")
        input("Press any key to retry...")
        login(database)
