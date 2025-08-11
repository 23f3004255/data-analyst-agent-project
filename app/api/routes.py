from typing import Optional
from fastapi import APIRouter, UploadFile,File
from app.config import FILE_PATH
from app.utils import read_question_file, extract_questions
from app.services import handle_request

router=APIRouter()

@router.get("/")
def hello():
    text=read_question_file(FILE_PATH)
    return extract_questions(text)


@router.post("/")
async def analyse(file:UploadFile=File(...),files: Optional[list[UploadFile]] = File(None)):
    return await handle_request(file,files)


