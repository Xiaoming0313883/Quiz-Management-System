from asset.useful import clear_console
from database.core import core
from database.manager import quizManager
import ui.dashboard as dashboard


def manageQuiz(database: core, userid):
    clear_console()
    options = ["List all quiz","View quiz information","Active/unactive quiz","Delete quiz","Go Back"]
    print("Choose the option to proceed")
    for index, name in enumerate(options, 1):
        print(f'{index}. {name}')
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
            quizManager.listAllQuiz(database, userid)
        case 2:
            quizManager.viewQuiz(database, userid)
        case 3:
            quizManager.setQuizStatus(database, userid)
        case 4:
            quizManager.deleteQuiz(database, userid)
        case 5:
            dashboard.teacher_dashboard(database, userid)
