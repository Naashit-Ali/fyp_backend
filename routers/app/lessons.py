# routers/app/lessons.py

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

class LessonLevelQuestionResponse(BaseModel):
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

    is_active: Annotated[Optional[bool], None] = None

class LessonLevelResponse(BaseModel):
    id: Annotated[Optional[int], None] = None
    title: Annotated[Optional[str], None] = None
    description: Annotated[Optional[str], None] = None

    no_of_questions: Annotated[Optional[int], None] = None
    questions: Annotated[List[LessonLevelQuestionResponse], None] = None

    status: Annotated[Optional[str], None] = None
    is_active: Annotated[Optional[bool], None] = None

class LessonResponse(BaseModel):
    id: Annotated[Optional[int], None] = None
    title: Annotated[Optional[str], None] = None
    description: Annotated[Optional[str], None] = None
    no_of_levels: Annotated[Optional[int], None] = None
    no_of_levels_completed: Annotated[Optional[int], None] = None
    levels: Annotated[List[LessonLevelResponse], None] = None
    is_active: Annotated[Optional[bool], None] = None

class CompleteLessonLevelRequest(BaseModel):
    lesson_level_id: Annotated[Optional[int], None] = None
    user_id: Annotated[Optional[int], None] = None
    questions_answered_correctly: Annotated[Optional[int], None] = None


@router.get('/getAllLessons/{user_id}', status_code=status.HTTP_200_OK, response_model=list[LessonResponse])
async def get_all_lessons(db: db_dependency, user_id: int = Path(..., ge=1)):
    try:
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found")

        # Lessons
        lessons = db.query(models.Lessons).filter(models.Lessons.is_active == 1).all()
        lessons_response = []
        for lesson in lessons:
            no_of_levels = db.query(func.count(models.Lesson_Levels.id)).filter(models.Lesson_Levels.lesson_id == lesson.id).scalar()
            no_of_levels_completed = db.query(func.count(models.Users_Lesson_Levels_Result.id)).filter(
                models.Users_Lesson_Levels_Result.lesson_level_id == models.Lesson_Levels.id,
                models.Lesson_Levels.lesson_id == lesson.id,
                models.Users_Lesson_Levels_Result.user_id == user_id,
                models.Users_Lesson_Levels_Result.status == "Completed"
            ).scalar()

            # Levels
            levels = db.query(models.Lesson_Levels).filter(models.Lesson_Levels.lesson_id == lesson.id, models.Lesson_Levels.is_active == 1).all()
            level_responses = []
            for level in levels:
                status = str(db.query(models.Users_Lesson_Levels_Result.status).filter(
                    models.Users_Lesson_Levels_Result.lesson_level_id == level.id,
                    models.Users_Lesson_Levels_Result.user_id == user_id
                ).scalar() or "")

                # Questions
                questions = db.query(models.Lesson_Questions).filter(
                    models.Lesson_Questions.lesson_level_id == level.id,
                    models.Lesson_Questions.is_active == 1,
                    models.Lesson_Questions.age_group == "7-9" if (user.age >= 7 and user.age <= 9) else models.Lesson_Questions.age_group == "10-12" if (user.age >= 10 and user.age <= 12) else None
                ).all()
                
                question_responses = []
                for question in questions:
                    question_response = LessonLevelQuestionResponse(
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

                        is_active=question.is_active
                    )
                    question_responses.append(question_response)

                level_response = LessonLevelResponse(
                    id=level.id,
                    title=level.title,
                    description=level.description,
                    is_active=level.is_active,
                    no_of_questions=level.no_of_questions,
                    status=status,
                    questions=question_responses
                )
                level_responses.append(level_response)

            lesson_response = LessonResponse(
                id=lesson.id,
                title=lesson.title,
                description=lesson.description,
                is_active=lesson.is_active,
                no_of_levels=no_of_levels,
                no_of_levels_completed=no_of_levels_completed,
                levels=level_responses
            )
            lessons_response.append(lesson_response)
        return lessons_response
    
    except ValueError as e:
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get('/getAllLessonLevels/{lesson_id}/{user_id}', status_code=status.HTTP_200_OK, response_model=list[LessonLevelResponse])
async def get_all_lesson_levels(db: db_dependency, lesson_id: int = Path(..., ge=1), user_id: int = Path(..., ge=1)):
    try:
        # Checking if lesson exists
        lesson = db.query(models.Lessons).filter(models.Lessons.id == lesson_id).first()
        if lesson is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Lesson not found")
        
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found")

        # Levels
        levels = db.query(models.Lesson_Levels).filter(models.Lesson_Levels.lesson_id == lesson_id, models.Lesson_Levels.is_active == 1).all()
        level_responses = []
        for level in levels:
            status = str(db.query(models.Users_Lesson_Levels_Result.status).filter(
                models.Users_Lesson_Levels_Result.lesson_level_id == level.id,
                models.Users_Lesson_Levels_Result.user_id == user_id
            ).scalar() or "")

            # Questions
            questions = db.query(models.Lesson_Questions).filter(
                models.Lesson_Questions.lesson_level_id == level.id,
                models.Lesson_Questions.is_active == 1,
                models.Lesson_Questions.age_group == "7-9" if (user.age >= 7 and user.age <= 9) else models.Lesson_Questions.age_group == "10-12" if (user.age >= 10 and user.age <= 12) else None
            ).all()
            
            question_responses = []
            for question in questions:
                question_response = LessonLevelQuestionResponse(
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

                    is_active=question.is_active
                )
                question_responses.append(question_response)

            level_response = LessonLevelResponse(
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
    

@router.get('/getLessonLevelQuestions/{lesson_level_id}/{user_id}', status_code=status.HTTP_200_OK)
async def get_lesson_level_questions(db: db_dependency, lesson_level_id: int = Path(..., ge=1), user_id: int = Path(..., ge=1)):
    try:
        # Checking if lesson level exists
        lesson_level = db.query(models.Lesson_Levels).filter(models.Lesson_Levels.id == lesson_level_id).first()
        if lesson_level is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Lesson Level not found")

        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found")

        # Questions
        questions = db.query(models.Lesson_Questions).filter(
            models.Lesson_Questions.lesson_level_id == lesson_level.id,
            models.Lesson_Questions.is_active == 1,
            models.Lesson_Questions.age_group == "7-9" if (user.age >= 7 and user.age <= 9) else models.Lesson_Questions.age_group == "10-12" if (user.age >= 10 and user.age <= 12) else None
        ).all()
        question_responses = []
        for question in questions:
            question_response = LessonLevelQuestionResponse(
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
    

@router.post('/completeLessonLevel', status_code=fastapi.status.HTTP_200_OK)
async def complete_lesson_level(db: db_dependency, request: CompleteLessonLevelRequest):
    try:
        lesson_level_id = request.lesson_level_id
        user_id = request.user_id
        questions_answered_correctly = request.questions_answered_correctly

        result = db.query(models.Users_Lesson_Levels_Result).filter_by(lesson_level_id=lesson_level_id, user_id=user_id).first()

        if result:
            result.status = "Completed" if questions_answered_correctly == result.lesson_level.no_of_questions else result.status
            db.add(result)
            db.commit()
            db.refresh(result)
        else:
            status = "Completed" if questions_answered_correctly == result.lesson_level.no_of_questions else "Unlocked"
            new_result = models.Users_Lesson_Levels_Result(lesson_level_id=lesson_level_id, user_id=user_id, status=status) 
            db.add(new_result)
            db.commit()
            db.refresh(new_result)

        return {"message": "Lesson level completed successfully"}

    except ValueError as e: 
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    