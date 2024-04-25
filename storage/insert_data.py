# storage/insert_data.py

import sys
sys.path.append('C:/Users/mehbo/Desktop/FYP-Backend')

from storage import data
from storage.queries import (get_db, insert_avatar, insert_user, 
                             insert_quiz, insert_quiz_level, insert_quiz_question, insert_users_quiz_levels_result,
                             insert_lesson, insert_lesson_level, insert_lesson_question, insert_users_lesson_levels_result)

def populate_avatars():
    db = next(get_db())
    for avatar in data.avatar_data:
        insert_avatar(db, **avatar)

def populate_users():
    db = next(get_db())
    for user in data.user_data:
        insert_user(db, **user)

def populate_quizzes():
    db = next(get_db())
    for quiz in data.quiz_data:
        insert_quiz(db, **quiz)

def populate_quiz_levels():
    db = next(get_db())
    for quiz_level in data.quiz_level_data:
        insert_quiz_level(db, **quiz_level)

def populate_quiz_questions():
    db = next(get_db())
    for quiz_question in data.quiz_question_data:
        insert_quiz_question(db, **quiz_question)

def populate_users_quiz_levels_results():
    db = next(get_db())
    for users_quiz_levels_result in data.users_quiz_levels_result_data:
        insert_users_quiz_levels_result(db, **users_quiz_levels_result)

def populate_lessons():
    db = next(get_db())
    for lesson in data.lesson_data:
        insert_lesson(db, **lesson)

def populate_lesson_levels():
    db = next(get_db())
    for lesson_level in data.lesson_level_data:
        insert_lesson_level(db, **lesson_level)

def populate_lesson_questions():
    db = next(get_db())
    for lesson_question in data.lesson_question_data:
        insert_lesson_question(db, **lesson_question)

def populate_users_lesson_levels_results():
    db = next(get_db())
    for users_lesson_levels_result in data.users_lesson_levels_result_data:
        insert_users_lesson_levels_result(db, **users_lesson_levels_result)


if __name__ == "__main__":
    populate_avatars()
    populate_users()
    populate_quizzes()
    populate_quiz_levels()
    populate_quiz_questions()
    populate_users_quiz_levels_results()
    populate_lessons()
    populate_lesson_levels()
    populate_lesson_questions()
    populate_users_lesson_levels_results()
