from fastapi import FastAPI, Depends

app = FastAPI()

def get_message():
    return "Hello FastAPI"

@app.get('/hello')
def hello(
    msg1 = Depends(get_message),
    msg2 = Depends(get_message)
):
    return {
        "msg1" : msg1,
        "msg2" : msg2
    }
    
def get_number():
    print("Executed")
    return 10

@app.get("/")
def root(
    a=Depends(get_number),
    b=Depends(get_number),
    c=Depends(get_number)
):
    return {
        "a": a,
        "b": b,
        "c": c
    }