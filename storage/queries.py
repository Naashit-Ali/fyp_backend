# storage/queries.py

from fastapi import APIRouter, Depends
from typing import Annotated
import database.models as models
from database.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def insert_avatar(db: db_dependency, image, title="Sample title", description="Sample Description", is_active=True):
    new_avatar = models.Avatars(
        title=title,
        description=description,
        image=image,
        is_active=is_active
    )
    db.add(new_avatar)
    db.commit()

def insert_user(db: db_dependency, username, age, password, description, avatar_id=1, exp_points=0, is_active=True):
    new_user = models.Users(
        avatar_id=avatar_id,
        username=username,
        description=description,
        age=age,
        password=password,
        exp_points=exp_points,
        is_active=is_active
    )
    db.add(new_user)
    db.commit()

def insert_quiz(db: db_dependency, title="Sample title", description="Sample Description", is_active=True):
    new_quiz = models.Quizzes(
        title=title,
        description=description,
        is_active=is_active
    )
    db.add(new_quiz)
    db.commit()

def insert_quiz_level(db: db_dependency, quiz_id, title="Sample title", description="Sample Description", no_of_questions=0, is_active=True):
    new_quiz_level = models.Quiz_Levels(
        quiz_id=quiz_id,
        title=title,
        description=description,
        no_of_questions=no_of_questions,
        is_active=is_active
    )
    db.add(new_quiz_level)
    db.commit()

def insert_quiz_question(db: db_dependency, quiz_level_id, age_group, 
                         question_type, question_text, arabic_text, arabic_text_audio, question_image, question_audio, question_video,
                         answer_type, correct_option, option1, option2, option3, option4,
                         title="Sample title", description="Sample Description", is_active=True):
    new_quiz_question = models.Quiz_Questions(
        quiz_level_id=quiz_level_id,

        title=title,
        description=description,
        age_group=age_group,

        question_type=question_type,
        question_text=question_text,
        arabic_text=arabic_text,
        arabic_text_audio=arabic_text_audio,
        question_image=question_image,
        question_audio=question_audio,
        question_video=question_video,

        answer_type=answer_type,
        correct_option=correct_option,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,

        is_active=is_active
    )
    db.add(new_quiz_question)
    db.commit()

def insert_users_quiz_levels_result(db: db_dependency, user_id, quiz_level_id, status="Locked"):
    new_users_quiz_levels_result = models.Users_Quiz_Levels_Result(
        user_id=user_id,
        quiz_level_id=quiz_level_id,
        status=status
    )
    db.add(new_users_quiz_levels_result)
    db.commit()

def insert_lesson(db: db_dependency, title="Sample title", description="Sample Description", is_active=True):
    new_lesson = models.Lessons(
        title=title,
        description=description,
        is_active=is_active
    )
    db.add(new_lesson)
    db.commit()

def insert_lesson_level(db: db_dependency, lesson_id, title="Sample title", description="Sample Description", no_of_questions=0, is_active=True):
    new_lesson_level = models.Lesson_Levels(
        lesson_id=lesson_id,
        title=title,
        description=description,
        no_of_questions=no_of_questions,
        is_active=is_active
    )
    db.add(new_lesson_level)
    db.commit()

def insert_lesson_question(db: db_dependency, lesson_level_id, age_group, 
                         question_type, question_text, arabic_text, arabic_text_audio, question_image, question_audio, question_video,
                         title="Sample title", description="Sample Description", is_active=True):
    new_lesson_question = models.Lesson_Questions(
        lesson_level_id=lesson_level_id,

        title=title,
        description=description,
        age_group=age_group,

        question_type=question_type,
        question_text=question_text,
        arabic_text=arabic_text,
        arabic_text_audio=arabic_text_audio,
        question_image=question_image,
        question_audio=question_audio,
        question_video=question_video,

        is_active=is_active
    )
    db.add(new_lesson_question)
    db.commit()

def insert_users_lesson_levels_result(db: db_dependency, user_id, lesson_level_id, status="Locked"):
    new_users_lesson_levels_result = models.Users_Lesson_Levels_Result(
        user_id=user_id,
        lesson_level_id=lesson_level_id,
        status=status
    )
    db.add(new_users_lesson_levels_result)
    db.commit()