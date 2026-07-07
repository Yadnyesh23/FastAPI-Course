from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {
    "message":"Student API"
    }
    
@app.get('/students')
#Internally this does 
#app.router.add_route(
#     path="/students",
#     method="GET",
#     function=get_students
# )
def get_students():
    return [
    {
        "id":1,
        "name":"Yadnyesh"
    },
    {
        "id":2,
        "name":"Rahul"
    }
]
    
@app.post("/students")
def create_student():
    return {
    "message":"Student Created"
}
    
@app.put('/students/1')
def put_student():
    return {
    "message":"Student Updated"
}
    
@app.patch('/students/1')
def patch_student():
    return {
    "message":"Student Partially Updated"
}
    
@app.delete('/students/1')
def delete_student():
    return {
    "message":"Student deleted"
}