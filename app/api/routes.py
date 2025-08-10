from fastapi import APIRouter
from app.config import FILE_PATH
from app.utils import read_question_file,extract_questions

router=APIRouter()

@router.get("/")
def hello():
    text=read_question_file(FILE_PATH)
    return extract_questions(text)



