from fastapi import FastAPI, Header, Response, Cookie

app = FastAPI()

@app.get("/user-agent")
def get_user_agent(
    user_agent: str = Header()
):
    return {
        "user_agent": user_agent
    }

@app.get('/student')
def get_student(
  student_id : str = Header(
      alias = "X-Student-Id"
  )  
):
    return {
        "student_id" : student_id
    }
    
@app.get('/login')
def login(response : Response):
    response.set_cookie(
        key="session_id",
        value="abc123"
    )
    return {
        "message" : "Logged-in"
    }

@app.get("/profile")
def profile(
    session_id: str = Cookie()
):
    return {
        "session_id": session_id
    }

@app.get("/logout")
def logout(response: Response):

    response.delete_cookie(
        key="session_id"
    )

    return {
        "message": "Logged out"
    }