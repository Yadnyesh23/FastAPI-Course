from fastapi import FastAPI
app = FastAPI()

@app.get('/books')
def get_book(title : str):
    return {
        "title" : title
    }

@app.get('/movies')
def get_movies(year : int, genre : str):
    return {
        "Year" : year,
        "Genre" : genre
    }
    
@app.get('/students')
def get_students(page : int = 1):
    return {
        "page" : page
    }
    
@app.get('/users')
def get_students(active : bool = False):
    return {
        "page" : active
    }
    
@app.get('/students/{student_id}')
def get_students(students_id : int, include_marks : bool = False):
    return {
        "page" : include_marks
    }
    