from asset.useful import clear_console
from database.core import core
from database.manager.quizManager import createQuiz
import ui.dashboard as dashboard

def create_quiz(database: core,user_id):
    clear_console()
    while True:
        count = input("How many questions do you want?: ")
        if not count.isdigit():
            print("Please enter a number")
            continue
        break
    title = input("What is the title of the quiz?: ")
    description = input("What is the description of the quiz?: ")
    quiz = {"user_id": user_id, "title": title, "description": description, "quiz": []}
    for i in range (int(count)):
        question = input("Enter question " + str(i + 1) + ":")
        a = input("A: ")
        b = input("B: ")
        c = input("C: ")
        d = input("D: ")
        while True:
            answer = input("Answer (A/B/C/D): ")
            if answer.lower() not in ["a", "b", "c", "d"]:
                print("Answer must be A/B/C/D")
                continue
            break
        quiz["quiz"].append({"question":question,"A": a, "B": b, "C": c, "D": d, "answer":answer})

    confirm = input("Do you wish to save the quiz? (y/n): ")
    if confirm.lower() == "y":
        status, quiz_id = createQuiz(database, quiz)
        if status:
            print(f"Quiz created successfully! Quiz ID: {quiz_id}")
        else:
            print("Quiz creation failed, try again later")
    else:
        print("Quiz creation cancelled")
    input("Press any key to continue...")
    dashboard.teacher_dashboard(database, user_id)