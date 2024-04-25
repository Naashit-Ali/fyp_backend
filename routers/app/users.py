# routers/app/users.py

from fastapi import APIRouter, Path, Query, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Optional
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

class AvatarResponse(BaseModel):
    id: Annotated[Optional[int], None] = None
    title: Annotated[str, None] = None
    description: Annotated[Optional[str], None] = None
    image: Annotated[Optional[str], None] = None
    is_active: Annotated[Optional[bool], None] = None

class UserResponse(BaseModel):
    id: Annotated[Optional[int], None] = None
    username: Annotated[Optional[str], None] = None
    description: Annotated[Optional[str], None] = None
    age: Annotated[Optional[int], None] = None
    exp_points: Annotated[Optional[int], None] = None
    avatar_id: Annotated[Optional[int], None] = None
    avatar: Annotated[AvatarResponse, None] = None
    is_active: Annotated[Optional[bool], None] = None

class UserUpdate(BaseModel):
    username: Annotated[Optional[str], None, Field(min_length=1, max_length=45)] = None
    description: Annotated[Optional[str], None, Field(min_length=1, max_length=255)] = None
    age: Annotated[Optional[int], None, Field(ge=1, le=100)] = None
    avatar_id: Annotated[Optional[int], None, Field(ge=1), ] = None
    is_active: Annotated[Optional[bool], None] = None
    

# Signup api using username, age, and password
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(db: db_dependency, username: str = Query(..., min_length=1, max_length=45), age: int = Query(..., gt=0, le=100), password: str = Query(..., min_length=1, max_length=100)):
    try:
        # Checking if a user with same username already exists
        existing_user = db.query(models.Users).filter(models.Users.username == username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        # Create new user
        new_user = models.Users(username=username, age=age, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Signin api using username and password
@router.post('/signin', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def signin(db: db_dependency, username: str = Query(..., min_length=1, max_length=45), password: str = Query(..., min_length=1, max_length=100)):
    try:        
        # Check if user exists
        db_user = db.query(models.Users).filter(models.Users.username == username).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # Check if user is active
        if not db_user.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is inactive")
        # Check if password is correct
        if db_user.password != password:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong password")
        
        return db_user
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# GetProfile api
@router.get('/getProfile/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_profile(db: db_dependency, user_id: int = Path(..., gt=0)):
    try:
        # Checking if user exists and is active
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is inactive")
        
        return user
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# UpdateProfile api
@router.put('/updateProfile/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_profile(user_update: UserUpdate, db: db_dependency, user_id: int = Path(..., gt=0)):
    try:
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user_update.username is not None:
            user.username = user_update.username
        if user_update.description is not None:
            user.description = user_update.description
        if user_update.age is not None:
            user.age = user_update.age
        # Checking if avatar_id exists and is active
        if user_update.avatar_id is not None:
            avatar = db.query(models.Avatars).filter(models.Avatars.id == user_update.avatar_id).first()
            if avatar is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
            if avatar.is_active != 1:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Avatar is inactive. An avatar needs to active to be used.")
            user.avatar_id = user_update.avatar_id
        if user_update.is_active is not None:
            user.is_active = user_update.is_active

        db.commit()
        db.refresh(user)
        return user
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# getAvatars api
@router.get('/getAvatars', status_code=status.HTTP_200_OK, response_model=list[AvatarResponse])
async def get_avatars(db: db_dependency):
    try:
        avatars = db.query(models.Avatars).filter(models.Avatars.is_active == 1).all()
        if not avatars:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No avatars found")
        return avatars
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# updateAvatar api
@router.put('/updateUserAvatar/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_avatar(db: db_dependency, user_id: int = Path(..., ge=1), avatar_id: int = Query(..., gt=0)):
    try:
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Checksing if avatar_id exists and is active
        if avatar_id is not None:
            avatar = db.query(models.Avatars).filter(models.Avatars.id == avatar_id).first()
            if avatar is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
            if avatar.is_active != 1:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Avatar is inactive. An avatar needs to active to be used.")
            user.avatar_id = avatar_id

        db.commit()
        db.refresh(user)
        return user
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# logout api (can't make for now since no bearer token system is implemented)
    
# updatePassword api
@router.put('/updatePassword/{user_id}', status_code=status.HTTP_200_OK)
async def update_password(db: db_dependency, user_id: int = Path(..., gt=0), old_password: str = Query(..., min_length=1, max_length=100), new_password: str = Query(..., min_length=1, max_length=100)):
    try:
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Checking if old password is correct
        if user.password != old_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong old password")
        if user.password == new_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password is same as old password")

        user.password = new_password
        db.commit()
        return {"message": "Password updated successfully"}
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# deleteAccount api
@router.delete('/deleteAccount/{user_id}', status_code=status.HTTP_200_OK)
async def delete_account(db: db_dependency, user_id: int = Path(..., gt=0), password: str = Query(..., min_length=1, max_length=100)):
    try:
        # Checking if user exists
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user.password != password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")

        db.delete(user)
        db.commit()
        return {"message": "Account Deleted successfully"}

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

