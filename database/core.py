from config_env import env_vars
import mysql.connector
from database.manager import userManager
from asset.timeCount import TimeCount

class core:

    def __init__(self):
        host = env_vars.get("DB_HOST")
        user = env_vars.get("DB_USER")
        password = env_vars.get("DB_PASSWORD")
        port = env_vars.get("DB_PORT")
        try:
            self.db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                port=port
            )
            self.db_connection.autocommit = True
        except mysql.connector.Error as err:
            print(err)
            exit(1)

        if self.db_connection.is_connected():
            print("Connected to Database!")

        cursor = self.db_connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'quiz'")
        if cursor.fetchone():
            print("Database exists!")
            cursor.execute("USE quiz")
        else:
            print("Database does not exist. Creating new database and initialize...")
            self.initialize_database()

    def initialize_database(self):
        timeCount = TimeCount().start()
        cursor = self.db_connection.cursor()
        cursor.execute("""
                DROP DATABASE IF EXISTS `quiz`;
                CREATE DATABASE `quiz`;
                USE `quiz`;
                CREATE TABLE `users` (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    role ENUM('teacher', 'student') NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
    
                CREATE TABLE quizzes (
                    quiz_id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_by INT NOT NULL,
                    status ENUM('active','inactive') NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
    
                CREATE TABLE questions (
                    question_no INT NOT NULL,
                    quiz_id INT NOT NULL,
                    question_text TEXT NOT NULL,
                    option_a VARCHAR(255) NOT NULL,
                    option_b VARCHAR(255) NOT NULL,
                    option_c VARCHAR(255) NOT NULL,
                    option_d VARCHAR(255) NOT NULL,
                    correct_option ENUM('A','B','C','D') NOT NULL,
    
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB;
    
                CREATE TABLE attempts (
                    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
                    quiz_id INT NOT NULL,
                    user_id INT NOT NULL,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME,
                    time_used FLOAT COMMENT 'Time used in seconds',
                    score INT DEFAULT 0,
    
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB;
    
                CREATE TABLE answers (
                    answer_id INT AUTO_INCREMENT PRIMARY KEY,
                    attempt_id INT NOT NULL,
                    quiz_id INT NOT NULL,
                    question_id INT NOT NULL,
                    selected_option ENUM('A','B','C','D') NOT NULL,
                    correct_option ENUM('A','B','C','D') NOT NULL,
                    is_correct TINYINT(1) NOT NULL,
    
                    FOREIGN KEY (attempt_id)
                    REFERENCES attempts(attempt_id)
                    ON DELETE CASCADE,
            
                    FOREIGN KEY (quiz_id)
                    REFERENCES questions(quiz_id)
                    ON DELETE CASCADE
                ) ENGINE=InnoDB;
    
                """)
        timeCount.stop().broadcast()
        userManager.create_user(
            dbase=self,
            username="admin",
            password="123",
            full_name="Administrator",
            role=userManager.Role.teacher
        )
        print("Default username = admin password = 123")