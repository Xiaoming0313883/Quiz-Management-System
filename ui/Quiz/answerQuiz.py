import time

import asset.useful
from asset.useful import clear_console
from database.core import core
from database.manager import quizManager, userManager
import ui.dashboard as dashboard

def answerQuiz(database: core, user_id):
    clear_console()
    quiz_id, data = quizManager.checkQuizIdValid(database)
    answered = quizManager.isStudentAnswered(database, user_id, quiz_id)
    is_active = quizManager.isQuizActive(database, quiz_id)
    if answered:
        print("Quiz already answered!")
    if data and not answered and is_active:
        clear_console()
        title = data[0]
        description = data[1]
        status, created_by = userManager.getUsernameByID(database, data[2])
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Created By: {created_by}")
        questions = quizManager.getQuiz(database, quiz_id)
        answers = {"quiz_id": quiz_id, "user_answer": {}}
        start_time = time.time()
        score = 0
        max_score = len(questions)
        for question in questions:
            question_no = question[0]
            question_text = question[1]
            option_a = question[2]
            option_b = question[3]
            option_c = question[4]
            option_d = question[5]
            answer = question[6]
            print(f"Question {question_no}: {question_text}")
            print(f"A: {option_a}")
            print(f"B: {option_b}")
            print(f"C: {option_c}")
            print(f"D: {option_d}")
            while True:
                user_answer = input("Enter your answer (A/B/C/D): ")
                if user_answer.lower() not in ["a", "b", "c", "d"]:
                    print("Invalid answer.")
                    continue
                break
            correct = 0
            if user_answer.upper() == answer:
                correct = 1
                score += 1
            answers["user_answer"][question_no] = {
                "question_no": question_no,
                "answer": user_answer,
                "correct_answer": answer,
                "is_correct": correct,
            }
        end_time = time.time()
        answers["start_time"] = asset.useful.timestampToDateTime(start_time)
        answers["end_time"] = asset.useful.timestampToDateTime(end_time)
        answers["time_used"] = round(end_time - start_time, 2)
        answers["student_id"] = user_id
        answers["score"] = score
        status = quizManager.saveQuizAttempt(database, user_id, answers)
        if status:
            print("Quiz saved!")
            print(f"Score: {score}/{max_score}")
            print(f"Time taken: {(end_time - start_time):.2f} seconds")
        else:
            print("Quiz could not saved! Please try answer again")
    input("Press any key to go back...")
    dashboard.student_dashboard(database, user_id)
