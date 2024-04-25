# database/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import SessionLocal
from sqlalchemy.orm import Session


class Avatars(Base):
    __tablename__ = 'avatars'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    
    title = Column(String(45), unique=True, nullable=True)
    description = Column(String(255), nullable=True)
    image = Column(String(255), nullable=False, default='/assests/img/sampleavatar.jpg')
    
    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    avatar_id = Column(Integer, ForeignKey('avatars.id'), default=1, nullable=True)
    avatar = relationship('Avatars', backref='users')

    username = Column(String(45), unique=True, nullable=False)
    description = Column(String(255), default="Sample description", nullable=True)
    age = Column(Integer, nullable=False)
    password = Column(String(100), nullable=False)
    exp_points = Column(Integer, default=0, nullable=False)

    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Quizzes(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    
    title = Column(String(45), unique=True, nullable=True)
    description = Column(String(255), nullable=True)

    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Quiz_Levels(Base):
    __tablename__ = 'quiz_levels'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    quiz = relationship('Quizzes', backref='quiz_levels')

    title = Column(String(45), nullable=True)
    description = Column(String(255), nullable=True)
    no_of_questions = Column(Integer, nullable=False)

    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Quiz_Questions(Base):
    __tablename__ = 'quiz_questions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    quiz_level_id = Column(Integer, ForeignKey('quiz_levels.id'), nullable=False)
    quiz_level = relationship('Quiz_Levels', backref='quiz_questions')

    title = Column(String(45), unique=True, nullable=True)
    description = Column(String(255), nullable=True)
    age_group = Column(String(45), nullable=False)

    question_type = Column(String(45), nullable=False)
    question_text = Column(String(255), nullable=False)
    arabic_text = Column(String(255), nullable=True)
    arabic_text_audio = Column(String(255), nullable=True)
    question_image = Column(String(255), nullable=True)
    question_audio = Column(String(255), nullable=True)
    question_video = Column(String(255), nullable=True)

    #answer_type = 'text', 'image', 'audio', 'video'
    answer_type = Column(String(45), nullable=False)
    correct_option = Column(String(45), nullable=False)
    option1 = Column(String(255), nullable=False)
    option2 = Column(String(255), nullable=False)
    option3 = Column(String(255), nullable=False)
    option4 = Column(String(255), nullable=False)

    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Users_Quiz_Levels_Result(Base):
    __tablename__ = 'users_quiz_levels_result'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    quiz_level_id = Column(Integer, ForeignKey('quiz_levels.id'), nullable=False)
    quiz_level = relationship('Quiz_Levels', backref='users_quiz_levels_result')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('Users', backref='users_quiz_levels_result')

    #status = Locked, Unlocked, Completed
    status = Column(String(45), default='Locked', nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Lessons(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    
    title = Column(String(45), unique=True, nullable=True)
    description = Column(String(255), nullable=True)

    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Lesson_Levels(Base):
    __tablename__ = 'lesson_levels'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    lesson = relationship('Lessons', backref='lesson_levels')

    title = Column(String(45), unique=True, nullable=True)
    description = Column(String(255), nullable=True)
    no_of_questions = Column(Integer, nullable=False)

    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Lesson_Questions(Base):
    __tablename__ = 'lesson_questions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    lesson_level_id = Column(Integer, ForeignKey('lesson_levels.id'), nullable=False)
    lesson_level = relationship('Lesson_Levels', backref='lesson_questions')

    title = Column(String(45), unique=True, nullable=True)
    description = Column(String(255), nullable=True)
    age_group = Column(String(45), nullable=False)

    question_type = Column(String(45), nullable=False)
    question_text = Column(String(255), nullable=False)
    arabic_text = Column(String(255), nullable=True)
    arabic_text_audio = Column(String(255), nullable=True)
    question_image = Column(String(255), nullable=True)
    question_audio = Column(String(255), nullable=True)
    question_video = Column(String(255), nullable=True)

    #is_active = True, False
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Users_Lesson_Levels_Result(Base):
    __tablename__ = 'users_lesson_levels_result'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    lesson_level_id = Column(Integer, ForeignKey('lesson_levels.id'), nullable=False)
    lesson_level = relationship('Lesson_Levels', backref='users_lesson_levels_result')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('Users', backref='users_lesson_levels_result')

    #status = Locked, Unlocked, Completed
    status = Column(String(45), default='Locked', nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
