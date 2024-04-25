# /main.py

from fastapi import FastAPI
from routers.app import users, quizzes, lessons  # Importing routers from the routers package
import database.models as models
from database.database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = ["http://localhost:19006"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

# Include Routers
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["Quizzes"])
app.include_router(lessons.router, prefix="/api/v1/lessons", tags=["Lessons"])

@app.get("/")
def read_root():
    return {"Message": "You're connected to the Islamic Game API."}
