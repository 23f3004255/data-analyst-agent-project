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
async def analyse(file:UploadFile=File(...),files: list[UploadFile] = File(None)):
    return await handle_request(file,files)

    # content = await file.read()
    # content = content.decode("utf-8")
    # print(extract_questions(content))
    # print({"filename": file.filename, "size": len(content)})
    # return extract_questions(content)


