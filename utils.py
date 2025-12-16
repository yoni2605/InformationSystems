import mysql.connector
from contextlib import contextmanager
import os


DB_HOST = os.environ.get("DB_HOST", "PASTE YOUR HOST HERE")
DB_USER = os.environ.get("DB_USER", "PASTE YOUR USER HERE")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "PASTE YOUR PASSWORD HERE")
DB_NAME = os.environ.get("DB_NAME", "PASTE YOUR NAME HERE")


@contextmanager
def db_cur():
    mydb = None
    cursor = None
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=True,
            connection_timeout=5
        )
        cursor = mydb.cursor()
        yield cursor
    except mysql.connector.Error as err:
        raise err
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()


def get_phase():
    with db_cur() as cursor:
        cursor.execute("SELECT value_ FROM Meta WHERE key_='phase'")
        phase = cursor.fetchone()
    return phase[0] if phase else 'idle'


def get_answered(user_name):
    with db_cur() as cursor:
        cursor.execute("SELECT id FROM User_question_answers WHERE user_name = %s",(user_name,))
        rows = cursor.fetchall()

    answered_ids = [int(row[0]) for row in rows]
    return answered_ids


def add_answered(user_name, question_id):
    with db_cur() as cursor:
        cursor.execute("INSERT INTO User_question_answers (user_name, id) VALUES (%s, %s)",(user_name, question_id))


def set_phase(phase):
    with db_cur() as cursor:
        cursor.execute("UPDATE Meta SET value_=%s WHERE key_='phase'", (phase,))


def reset_db():
    with db_cur() as cursor:
        cursor.execute("TRUNCATE TABLE Users")
        cursor.execute("TRUNCATE TABLE Questions")
        cursor.execute("TRUNCATE TABLE User_question_answers")
        cursor.execute("UPDATE Meta SET value_='idle' WHERE key_='phase'")


def ensure_user(user_name):
    try:
        with db_cur() as cursor:
            cursor.execute("INSERT INTO Users (user_name, correct_answers) VALUES (%s, 0)", (user_name,))
            return True
    except mysql.connector.Error:
        return False


def get_scores():
    with db_cur() as cursor:
        cursor.execute("SELECT user_name, correct_answers FROM Users ORDER BY correct_answers DESC")
        scores = cursor.fetchall()
        return scores


def get_score(user_name):
    with db_cur() as cursor:
        cursor.execute("SELECT correct_answers FROM Users WHERE user_name = %s", (user_name,))
        score = cursor.fetchone()[0]
        return score


def inc_user_score(user_name, delta=1):
    with db_cur() as cursor:
        cursor.execute("UPDATE Users SET correct_answers = correct_answers + %s WHERE user_name=%s",
                       (delta, user_name,))


class Question:
    def __init__(self, question, correct_answer, wrong_answer1, wrong_answer2):
        self.question = question
        self.correct_answer = correct_answer
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2

    @staticmethod
    def add(q):
        try:
            with db_cur() as cursor:
                cursor.execute(
                    """INSERT INTO Questions (question, correct_answer, wrong_answer1, wrong_answer2)
                     VALUES (%s,%s,%s,%s)""", (q.question, q.correct_answer, q.wrong_answer1, q.wrong_answer2))
            return True
        except mysql.connector.Error:
            return False

    @staticmethod
    def all_questions():
        with db_cur() as cursor:
            cursor.execute("SELECT id, question FROM Questions")
            questions = cursor.fetchall()
            return questions

    @staticmethod
    def get(q_id):
        with db_cur() as cursor:
            cursor.execute("""SELECT question, correct_answer, wrong_answer1, wrong_answer2
                           FROM Questions WHERE id=%s""", (q_id,))
            row = cursor.fetchone()
            q = Question(*row)
        return q
