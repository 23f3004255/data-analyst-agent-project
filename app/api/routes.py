import os
import tempfile
from fastapi import APIRouter, UploadFile,File
from app.config import FILE_PATH
from app.utils import read_question_file, extract_questions, read_uploaded_file

router=APIRouter()

@router.get("/")
def hello():
    text=read_question_file(FILE_PATH)
    return extract_questions(text)


@router.post("/")
async def analyse(file:UploadFile=File(...)):
    pass


