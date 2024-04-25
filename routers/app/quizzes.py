# routers/app/quizzes.py

import fastapi
from fastapi import APIRouter, Path, Query, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, List, Dict, Optional
import database.models as models
from database.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class QuizLevelQuestionOptionResponse(BaseModel):
    option1: Annotated[Optional[str], None] = None
    option2: Annotated[Optional[str], None] = None
    option3: Annotated[Optional[str], None] = None
    option4: Annotated[Optional[str], None] = None

class QuizLevelQuestionResponse(BaseModel):
    id: Annotated[Optional[int], None] = None
    title: Annotated[Optional[str], None] = None
    description: Annotated[Optional[str], None] = None
    age_group: Annotated[Optional[str], None] = None

    question_type: Annotated[Optional[str], None] = None
    question_text: Annotated[Optional[str], None] = None
    arabic_text: Annotated[Optional[str], None] = None
    arabic_text_audio: Annotated[Optional[str], None] = None
    question_image: Annotated[Optional[str], None] = None
    question_audio: Annotated[Optional[str], None] = None
    question_video: Annotated[Optional[str], None] = None

    answer_type: Annotated[Optional[str], None] = None
    options: Annotated[QuizLevelQuestionOptionResponse, None] = None
    correct_answer: Annotated[Optional[str], None] = None

    is_active: Annotated[Optional[bool], None] = None

class QuizLevelResponse(BaseModel):
    id: Annotated[Optional[int], None] = None
    title: Annotated[Optional[str], None] = None
    description: Annotated[Optional[str], None] = None

    no_of_questions: Annotated[Optional[int], None] = None
    questions: Annotated[List[QuizLevelQuestionResponse], None] = None

    status: Annotated[Optional[str], None] = None
    is_active: Annotated[Optional[bool], None] = None

class QuizResponse(BaseModel):
    id: Annotated[Optional[int], None] = None
    title: Annotated[Optional[str], None] = None
    description: Annotated[Optional[str], None] = None
    no_of_levels: Annotated[Optional[int], None] = None
    no_of_levels_completed: Annotated[Optional[int], None] = None
    levels: Annotated[List[QuizLevelResponse], None] = None
    is_active: Annotated[Optional[bool], None] = None

class CompleteQuizLevelRequest(BaseModel):
    quiz_level_id: Annotated[Optional[int], None] = None
    user_id: Annotated[Optional[int], None] = None
    questions_answered_correctly: Annotated[Optional[int], None] = None

@router.get('/getAllQuizzes/{user_id}', status_code=status.HTTP_200_OK, response_model=list[QuizResponse])
async def get_all_quizzes(db: db_dependency, user_id: int = Path(..., ge=1)):
    try:
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found")

        # Quizzes
        quizzes = db.query(models.Quizzes).filter(models.Quizzes.is_active == 1).all()
        quizzes_response = []
        for quiz in quizzes:
            no_of_levels = db.query(func.count(models.Quiz_Levels.id)).filter(models.Quiz_Levels.quiz_id == quiz.id).scalar()
            no_of_levels_completed = db.query(func.count(models.Users_Quiz_Levels_Result.id)).filter(
                models.Users_Quiz_Levels_Result.quiz_level_id == models.Quiz_Levels.id,
                models.Quiz_Levels.quiz_id == quiz.id,
                models.Users_Quiz_Levels_Result.user_id == user_id,
                models.Users_Quiz_Levels_Result.status == "Completed"
            ).scalar()

            # Levels
            levels = db.query(models.Quiz_Levels).filter(models.Quiz_Levels.quiz_id == quiz.id, models.Quiz_Levels.is_active == 1).all()
            level_responses = []
            for level in levels:
                status = str(db.query(models.Users_Quiz_Levels_Result.status).filter(
                    models.Users_Quiz_Levels_Result.quiz_level_id == level.id,
                    models.Users_Quiz_Levels_Result.user_id == user_id
                ).scalar() or "")

                # Questions
                questions = db.query(models.Quiz_Questions).filter(
                    models.Quiz_Questions.quiz_level_id == level.id,
                    models.Quiz_Questions.is_active == 1,
                    models.Quiz_Questions.age_group == "7-9" if (user.age >= 7 and user.age <= 9) else models.Quiz_Questions.age_group == "10-12" if (user.age >= 10 and user.age <= 12) else None
                ).all()
                
                question_responses = []
                for question in questions:
                    options = QuizLevelQuestionOptionResponse(
                        option1=question.option1,
                        option2=question.option2,
                        option3=question.option3,
                        option4=question.option4
                    )
                    question_response = QuizLevelQuestionResponse(
                        id=question.id,
                        title=question.title,
                        description=question.description,
                        age_group=question.age_group,
                        
                        question_type=question.question_type,
                        question_text=question.question_text,
                        arabic_text=question.arabic_text,
                        arabic_text_audio=question.arabic_text_audio,
                        question_image=question.question_image,
                        question_audio=question.question_audio,
                        question_video=question.question_video,

                        answer_type=question.answer_type,
                        options=options,
                        correct_answer=question.correct_option,

                        is_active=question.is_active
                    )
                    question_responses.append(question_response)

                level_response = QuizLevelResponse(
                    id=level.id,
                    title=level.title,
                    description=level.description,
                    is_active=level.is_active,
                    no_of_questions=level.no_of_questions,
                    status=status,
                    questions=question_responses
                )
                level_responses.append(level_response)

            quiz_response = QuizResponse(
                id=quiz.id,
                title=quiz.title,
                description=quiz.description,
                is_active=quiz.is_active,
                no_of_levels=no_of_levels,
                no_of_levels_completed=no_of_levels_completed,
                levels=level_responses
            )
            quizzes_response.append(quiz_response)
        return quizzes_response
    
    except ValueError as e:
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/getAllQuizLevels/{quiz_id}/{user_id}', status_code=status.HTTP_200_OK, response_model=list[QuizLevelResponse])
async def get_all_quiz_levels(db: db_dependency, quiz_id: int = Path(..., ge=1), user_id: int = Path(..., ge=1)):
    try:
        # Checking if quiz exists
        quiz = db.query(models.Quizzes).filter(models.Quizzes.id == quiz_id).first()
        if quiz is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Quiz not found")
        
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found")

        # Levels
        levels = db.query(models.Quiz_Levels).filter(models.Quiz_Levels.quiz_id == quiz_id, models.Quiz_Levels.is_active == 1).all()
        level_responses = []
        for level in levels:
            status = str(db.query(models.Users_Quiz_Levels_Result.status).filter(
                models.Users_Quiz_Levels_Result.quiz_level_id == level.id,
                models.Users_Quiz_Levels_Result.user_id == user_id
            ).scalar() or "")

            # Questions
            questions = db.query(models.Quiz_Questions).filter(
                models.Quiz_Questions.quiz_level_id == level.id,
                models.Quiz_Questions.is_active == 1,
                models.Quiz_Questions.age_group == "7-9" if (user.age >= 7 and user.age <= 9) else models.Quiz_Questions.age_group == "10-12" if (user.age >= 10 and user.age <= 12) else None
            ).all()
            
            question_responses = []
            for question in questions:
                options = QuizLevelQuestionOptionResponse(
                    option1=question.option1,
                    option2=question.option2,
                    option3=question.option3,
                    option4=question.option4
                )
                question_response = QuizLevelQuestionResponse(
                    id=question.id,
                    title=question.title,
                    description=question.description,
                    age_group=question.age_group,
                    
                    question_type=question.question_type,
                    question_text=question.question_text,
                    arabic_text=question.arabic_text,
                    arabic_text_audio=question.arabic_text_audio,
                    question_image=question.question_image,
                    question_audio=question.question_audio,
                    question_video=question.question_video,

                    answer_type=question.answer_type,
                    options=options,
                    correct_answer=question.correct_option,

                    is_active=question.is_active
                )
                question_responses.append(question_response)

            level_response = QuizLevelResponse(
                id=level.id,
                title=level.title,
                description=level.description,
                is_active=level.is_active,
                no_of_questions=level.no_of_questions,
                status=status,
                questions=question_responses
            )
            level_responses.append(level_response)
        return level_responses
    
    except ValueError as e:
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/getQuizLevelQuestions/{quiz_level_id}/{user_id}', status_code=status.HTTP_200_OK)
async def get_quiz_level_questions(db: db_dependency, quiz_level_id: int = Path(..., ge=1), user_id: int = Path(..., ge=1)):
    try:
        # Checking if quiz level exists
        quiz_level = db.query(models.Quiz_Levels).filter(models.Quiz_Levels.id == quiz_level_id).first()
        if quiz_level is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Quiz Level not found")
        
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found")

        # Questions
        questions = db.query(models.Quiz_Questions).filter(
            models.Quiz_Questions.quiz_level_id == quiz_level.id,
            models.Quiz_Questions.is_active == 1,
            models.Quiz_Questions.age_group == "7-9" if (user.age >= 7 and user.age <= 9) else models.Quiz_Questions.age_group == "10-12" if (user.age >= 10 and user.age <= 12) else None
        ).all()
        question_responses = []
        for question in questions:
            options = QuizLevelQuestionOptionResponse(
                option1=question.option1,
                option2=question.option2,
                option3=question.option3,
                option4=question.option4
            )
            question_response = QuizLevelQuestionResponse(
                id=question.id,
                title=question.title,
                description=question.description,
                age_group=question.age_group,

                question_type=question.question_type,
                question_text=question.question_text,
                arabic_text=question.arabic_text,
                arabic_text_audio=question.arabic_text_audio,
                question_image=question.question_image,
                question_audio=question.question_audio,
                question_video=question.question_video,

                answer_type=question.answer_type,
                options=options,
                correct_answer=question.correct_option,

                is_active=question.is_active
            )
            question_responses.append(question_response)

        return question_responses
    
    except ValueError as e:
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/completeQuizLevel', status_code=fastapi.status.HTTP_200_OK)
async def complete_quiz_level(db: db_dependency, request: CompleteQuizLevelRequest):
    try:
        quiz_level_id = request.quiz_level_id
        user_id = request.user_id
        questions_answered_correctly = request.questions_answered_correctly

        result = db.query(models.Users_Quiz_Levels_Result).filter_by(quiz_level_id=quiz_level_id, user_id=user_id).first()

        if result:
            result.status = "Completed" if questions_answered_correctly == result.quiz_level.no_of_questions else result.status
            db.add(result)
            db.commit()
            db.refresh(result)
        else:
            status = "Completed" if questions_answered_correctly == result.quiz_level.no_of_questions else "Unlocked"
            new_result = models.Users_Quiz_Levels_Result(quiz_level_id=quiz_level_id, user_id=user_id, status=status) 
            db.add(new_result)
            db.commit()
            db.refresh(new_result)

        return {"message": "Quiz level completed successfully"}

    except ValueError as e: 
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
