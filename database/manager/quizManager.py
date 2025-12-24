from database.core import core
import mysql.connector
from tabulate import tabulate
from asset.useful import clear_console
from database.manager import userManager
import ui.dashboard as dashboard

def createQuiz(database: core, quiz_data):
    user_id = quiz_data["user_id"]
    quiz = quiz_data["quiz"]
    title = quiz_data["title"]
    description = quiz_data["description"]
    cursor = database.db_connection.cursor()
    cursor.execute(f"""
    INSERT INTO quiz.quizzes (title, description, created_by, status) VALUES (
        '{title}',
        '{description}',
        '{user_id}',
        'active'
    );
    """)
    quiz_id = cursor.lastrowid
    database.db_connection.commit()
    count = 0
    try:
        for i in quiz:
            count += 1
            question = i["question"]
            a = i["A"]
            b = i["B"]
            c = i["C"]
            d = i["D"]
            answer = i["answer"]
            cursor.execute(f"""INSERT INTO quiz.questions (question_no, quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option) VALUES (
                '{count}',
                '{quiz_id}',
                '{question}',
                '{a}',
                '{b}',
                '{c}',
                '{d}',
                '{answer}'
                );
            """)
        database.db_connection.commit()
        return True, quiz_id
    except mysql.connector.Error as err:
        print(err)
        return False, None

def checkQuizIdValid(database: core):
    try:
        cursor = database.db_connection.cursor()
        while True:
            data = None
            quiz_id = input("Enter quiz ID: ")
            if quiz_id == "exit":
                return False, False
            elif not quiz_id.isdigit():
                print("Please enter a valid quiz ID (number), enter exit to exit")
                continue
            cursor.execute(f"SELECT title, description, created_by, status, created_at FROM quiz.quizzes WHERE quiz_id = {quiz_id}")
            data = cursor.fetchone()
            if not data:
                print("No quiz with that ID, please try again! Type exit to exit")
                continue
            break
        return quiz_id, data
    except mysql.connector.Error:
        print("Something went wrong, please try again!")
        return False, None

def listAllQuiz(database: core,userid):
    cursor = database.db_connection.cursor()
    try:
        cursor.execute("SELECT * FROM quiz.quizzes")
        data = cursor.fetchall()
        datas = []
        for i in data:
            quiz_id = i[0]
            title = i[1]
            description = i[2]
            Status, creator = userManager.getUsernameByID(database, i[3])
            status = i[4]
            creation_date = i[5]
            datas.append([quiz_id, title, description, creator,status, creation_date])
        header = ["Quiz ID","Title","Description","Creator","Status", "Creation Date"]
        print(tabulate(datas, headers=header, tablefmt="grid"))
        input("Press any key to go back...")
        dashboard.teacher_dashboard(database,userid)

    except mysql.connector.Error as err:
        print(err)

def viewQuiz(database: core,userid):
    clear_console()
    quiz_id, data = checkQuizIdValid(database)
    if quiz_id:
        displayQuizInfo(database, quiz_id,data)
        listLeaderboard(database)
        viewStudent = input("Did you want to view student's answer? (y/n): ")
        if viewStudent.lower() == "y":
            username = input("Enter student username: ")
            user_id = userManager.getUseridByUsername(database, username)
            if user_id:
                status, attempt_id = getUserAnsweredQuiz(database, user_id, quiz_id)
                if status:
                    displayUserAnsweredQuiz(database, user_id, attempt_id)
                else:
                    print("The user didn't answer this quiz yet!")
            else:
                print("User not found!")
        input("Press any key to go back...")
    dashboard.teacher_dashboard(database, userid)

def listLeaderboard(database: core):
    try:
        cursor = database.db_connection.cursor()
        cursor.execute(f"SELECT u.full_name, u.username, a.start_time, a.end_time, a.time_used, a.score FROM quiz.users u INNER JOIN quiz.attempts a WHERE a.user_id = u.user_id ORDER BY a.start_time DESC;")
        data = cursor.fetchall()
        header = ["Full Name", "Username", "Start Time", "End Time", "Time Used", "Score"]
        print("Leaderboard:")
        print(tabulate(data, headers=header, tablefmt="grid"),"\n")
    except mysql.connector.Error:
        print("Something went wrong, please try again!")

def displayQuizHeaderInfo(database: core,quiz_id,data):
    quiz_title = data[0]
    quiz_description = data[1]
    status, quiz_creator = userManager.getUsernameByID(database, data[2])
    status = data[3]
    quiz_creation_date = data[4]
    print("Quiz ID: ", quiz_id)
    print("Quiz Title: ", quiz_title)
    print("Quiz Description: ", quiz_description)
    print("Quiz Creator: ", quiz_creator)
    print("Quiz Status: ", status)
    print("Quiz Creation Date: ", quiz_creation_date)

def displayQuizInfo(database: core,quiz_id,data):
    clear_console()
    try:
        datas = getQuiz(database, quiz_id)
        header = ["Question ID", "Question", "Option A", "Option B", "Option C", "Option D", "Answer"]
        displayQuizHeaderInfo(database, quiz_id, data)
        print("\nQuestion:")
        print(tabulate(datas, headers=header, tablefmt="grid"))
    except mysql.connector.Error as err:
        print(err)

def deleteQuiz(database: core,userid):
    clear_console()
    quiz_id, data = checkQuizIdValid(database)
    if quiz_id:
        print("Quiz Information")
        displayQuizInfo(database, quiz_id,data)
        confirm = input("\nAre you sure you want to delete this quiz? (y/n): ")
        if confirm.lower() == "y":
            try:
                cursor = database.db_connection.cursor()
                cursor.execute(f"DELETE FROM quiz.quizzes WHERE quiz_id = {quiz_id}")
                database.db_connection.commit()
                print("Quiz deleted successfully!")
            except mysql.connector.Error:
                print("You can't delete this quiz, please try again.")
        else:
            print("Action cancelled!")
        input("Press any key to go back...")
    dashboard.teacher_dashboard(database, userid)

def setQuizStatus(database: core,userid):
    clear_console()
    quiz_id, data = checkQuizIdValid(database)
    if quiz_id:
        print("Quiz Information")
        displayQuizInfo(database, quiz_id,data)
        status = input("\nSet the status of the quiz(active/inactive): ")
        cursor = database.db_connection.cursor()
        if status.lower() == "active":
            cursor.execute(f"UPDATE quiz.quizzes SET status='active' WHERE quiz_id = '{quiz_id}';")
            database.db_connection.commit()
            print("Quiz set as active!")
        elif status.lower() == "inactive":
            cursor.execute(f"UPDATE quiz.quizzes SET status='inactive' WHERE quiz_id = '{quiz_id}';")
            database.db_connection.commit()
            print("Quiz set as inactive!")
        else:
            print("Invalid input, action cancelled!")

    input("Press any key to go back...")
    dashboard.teacher_dashboard(database, userid)

def getQuiz(database: core,quizID):
    try:
        cursor = database.db_connection.cursor()
        cursor.execute(f"SELECT * FROM quiz.questions WHERE quiz_id = {quizID}")
        data = cursor.fetchall()
        datas = []
        for i in data:
            question_no = i[0]
            question_text = i[2]
            option_a = i[3]
            option_b = i[4]
            option_c = i[5]
            option_d = i[6]
            answer = i[7]
            datas.append([question_no, question_text, option_a, option_b, option_c, option_d, answer])
        return datas
    except mysql.connector.Error:
        print("Something wrong, please try again.")
        return False

def saveQuizAttempt(database: core,userid, data):
    start_time = data["start_time"]
    end_time = data["end_time"]
    time_used = data["time_used"]
    quiz_id = data["quiz_id"]
    score = data["score"]
    cursor = database.db_connection.cursor()
    try:
        cursor.execute(f"""INSERT INTO quiz.attempts (quiz_id, user_id, start_time, end_time, time_used, score) VALUES (
            '{quiz_id}',
            '{userid}',
            '{start_time}',
            '{end_time}',
            '{time_used}',
            '{score}'
        );""")
        database.db_connection.commit()
        attempt_id = cursor.lastrowid
        try:
            for answer in data["user_answer"].values():
                question_no = answer["question_no"]
                chosen_answer = answer["answer"]
                correct_answer = answer["correct_answer"]
                is_correct = answer["is_correct"]
                cursor.execute(f"""INSERT INTO quiz.answers (attempt_id, quiz_id, question_id, selected_option, correct_option, is_correct) VALUES (
                    '{attempt_id}',
                    '{quiz_id}',
                    '{question_no}',
                    '{chosen_answer}',
                    '{correct_answer}',
                    '{is_correct}'
                );""")
            database.db_connection.commit()
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
    except mysql.connector.Error as err:
        print(err)
        return False

def getAllAnsweredQuiz(database: core, userid):
    clear_console()
    try:
        cursor = database.db_connection.cursor()
        cursor.execute(f"""SELECT
            q.quiz_id,
            q.title,
            u.full_name,
            a.start_time,
            a.end_time,
            a.time_used,
            a.score
            FROM attempts a
            JOIN quizzes q ON a.quiz_id = q.quiz_id
            JOIN users u ON q.created_by = u.user_id
            WHERE a.user_id = '{userid}'
            ORDER BY a.start_time DESC;
        """)
        data = cursor.fetchall()
        header = ["Quiz ID", "Quiz Title", "Created By" ,"Start Time", "End Time", "Time Used", "Score"]
        print("Answered Quiz:")
        print(tabulate(data, headers=header, tablefmt="grid"))
    except mysql.connector.Error:
        print("Something went wrong")


def displayUserAnsweredQuiz(database: core, userid,attempt_id):
    cursor = database.db_connection.cursor()
    cursor.execute(f"""
        SELECT
            q.title,
            u.full_name,
            a.start_time,
            a.end_time,
            a.time_used,
            a.score
        FROM attempts a
        JOIN quizzes q ON a.quiz_id = q.quiz_id
        JOIN users u ON q.created_by = u.user_id
        WHERE a.attempt_id = '{attempt_id}';
    """)
    data = list(cursor.fetchone())
    data[2] = data[2].strftime("%Y-%m-%d %H:%M:%S")
    data[3] = data[3].strftime("%Y-%m-%d %H:%M:%S")
    data[4] = str(data[4])
    data[5] = str(data[5])
    status, full_name = userManager.getUsernameByID(database, userid)
    print(f"Quiz information for user: {full_name}")
    print("\nQuiz info: ")
    header = ["Title", "Created By", "Start Time", "End Time", "Time Used (s)", "Score"]
    print(tabulate([data], headers=header, tablefmt="grid"), "\n")

    cursor.execute(f"""
        SELECT
            q.question_no,
            q.question_text,
            q.option_a,
            q.option_b,
            q.option_c,
            q.option_d,
            q.correct_option,
            ans.selected_option,
            ans.is_correct
        FROM answers ans
        JOIN questions q ON ans.question_id = q.question_no
        WHERE ans.attempt_id = '{attempt_id}'
        ORDER BY q.question_no;
    """)
    data = cursor.fetchall()
    datas = []
    for row in data:
        datas.append([
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            "✔" if row[8] else "✘"
        ])
    print("Answer info: ")
    header = ["No", "Question", "A", "B", "C", "D", "Correct Answer", "Your Answer", "Score"]
    print(tabulate(datas, headers=header, tablefmt="grid"), "\n")

def getUserAnsweredQuiz(database: core, userid, quizID):
    clear_console()
    try:
        cursor = database.db_connection.cursor()
        cursor.execute(f"""SELECT attempt_id
            FROM quiz.attempts
            WHERE user_id = '{userid}'
              AND quiz_id = '{quizID}'
            ORDER BY start_time DESC
            LIMIT 1;
        """)
        data = cursor.fetchone()
        if data:
            attempt_id = data[0]
            return True, attempt_id
    except mysql.connector.Error:
        print("Something went wrong")
    return False, None


def UserGetAllAnsweredQuiz(database: core, userid):
    getAllAnsweredQuiz(database, userid)
    input("Press any key to go back...")
    dashboard.student_dashboard(database, userid)

def UserViewAnsweredQuiz(database: core, userid):
    getAllAnsweredQuiz(database, userid)
    quiz_id, data = checkQuizIdValid(database)
    if quiz_id:
        status, attempt_id = getUserAnsweredQuiz(database, userid, quiz_id)
        if status:
            displayUserAnsweredQuiz(database, userid, attempt_id)
            listLeaderboard(database)
        else:
            print("You didn't answer this quiz yet!")
    input("Press any key to go back...")
    dashboard.student_dashboard(database, userid)

def isUserAnswered(database: core, userid, quiz_id):
    try:
        cursor = database.db_connection.cursor()
        cursor.execute(f"""SELECT attempt_id
            FROM quiz.attempts
            WHERE user_id = '{userid}'
              AND quiz_id = '{quiz_id}'
            ORDER BY start_time DESC
            LIMIT 1;
        """)
        data = cursor.fetchone()
        if data:
            return True
    except mysql.connector.Error:
        print("Something went wrong")
    return False

def isQuizActive(database: core, quiz_id):
    try:
        cursor = database.db_connection.cursor()
        cursor.execute(f"""SELECT status FROM quiz.quizzes WHERE quiz_id = '{quiz_id}'""")
        data = cursor.fetchone()
        if data[0] == "active":
            return True
        return False
    except mysql.connector.Error:
        print("Something went wrong")
    return False