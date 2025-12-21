from asset.useful import clear_console
from database.core import core
from database.manager import userManager, quizManager
from ui import manageStudent
from ui.Quiz import answerQuiz, createQuiz, manageQuiz
from ui.manageStudent import manageStudent


def dashboard(database: core,data):
    clear_console()
    userid = data[0][0]
    fullname = data[0][1]
    role = data[0][2]
    print(f"Welcome {fullname}!")
    if role == userManager.Role.teacher.value:
        teacher_dashboard(database, userid)
    elif role == userManager.Role.student.value:
        student_dashboard(database, userid)

def determineDashboard(database: core, userid):
    role = userManager.getUserRole(database, userid)
    if role == userManager.Role.teacher.value:
        teacher_dashboard(database, userid)
    elif role == userManager.Role.student.value:
        student_dashboard(database, userid)

def teacher_dashboard(database: core,userid):
    options = ["Create a quiz","Manage quiz","Create an account","View all users","Delete a user"]
    print("------------------Dashboard------------------")
    print("Welcome to the Teacher Dashboard")
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
            #create a quiz
            createQuiz.create_quiz(database, userid)
        case 2:
            #manage quiz
            manageQuiz.manageQuiz(database, userid)
        case 3:
            #create a student account
            manageStudent.createUser(database, userid)
        case 4:
            #view all users
            manageStudent.viewAllUsers(database, userid)
        case 5:
            #delete a user
            manageStudent.deleteUser(database, userid)

def student_dashboard(database: core, userid):
    options = ["Answer a quiz", "View all answered quiz", "View answered quiz information"]
    print("------------------Dashboard------------------")
    print("Welcome to the Student Dashboard")
    print("Choose the option to proceed")
    for index, name in enumerate(options, 1):
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
            # answer a quiz
            answerQuiz.answerQuiz(database, userid)
        case 2:
            # view all answered quiz
            quizManager.StudentGetAllAnsweredQuiz(database, userid)
        case 3:
            # view answered quiz
            quizManager.StudentViewAnsweredQuiz(database, userid)
