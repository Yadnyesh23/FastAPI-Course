from fastapi import FastAPI, Depends

app = FastAPI()

def get_message():
    print("opening resourse")
    
    yield "Hello"
    
    print("closing resourse")

@app.get("/")
def root(
    msg=Depends(get_message)
):
    return {
        "message": msg
    }