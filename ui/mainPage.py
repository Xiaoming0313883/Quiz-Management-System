from asset.useful import clear_console
from database.core import core
from ui.login.login import login


def mainPage(database: core):
    clear_console()
    options = ["Login"]
    print("------------------Main Page------------------")
    print("Quiz Management System V1.0")
    print("Welcome to the Main Page")
    print("Choose the option to proceed")
    for index, name in enumerate(options,1):
        print(f'{index}. {name}')
    print("---------------------------------------------")
    while True:
        choose = input("Choose the option: ")
        if not choose.isdigit():
            print("Invalid input! Please enter a number.")
            continue
        choose = int(choose)
        if choose < 1 or choose > len(options):
            print("Invalid choice! Please select a valid option.")
            continue
        break

    match choose:
        case 1:
            login(database)