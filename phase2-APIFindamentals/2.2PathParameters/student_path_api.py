from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/students/{student_id}")
def get_student_by_id(student_id : int):
    return {
        "student_id" : student_id
    }
    
@app.get("/students/{student_id}/subject/{subject_name}")
def get_student_and_subject(student_id : int, subject_name : str):
    return {
    "student_id": student_id,
    "subject": subject_name
}
    
@app.get('/users/{username}')
def get_username(username : str):
    return {
    "username": username
}
    
@app.get('/products/{price}')
def get_username(price : float):
    return {
    "price": price
}
    
class LanguageName(str, Enum):
    python = "python"
    javascript = "javascript"
    cpp = "cpp"

@app.get('/language/{language_name}')
def get_language(language_name : LanguageName):
    return {
        "language_name" : language_name
    }
    